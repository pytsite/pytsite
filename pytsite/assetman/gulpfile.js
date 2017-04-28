var fs = require('fs');
var yargs = require('yargs');
var gulp = require('gulp');
var ignore = require('gulp-ignore');
var debug = yargs.argv.debug === 'yes';

function minifyJS(s) {
    var jsmin = require('gulp-minify');

    return s.pipe(jsmin({
        ext: {
            min: '.js'
        },
        noSource: true
    }));
}

function minifyCSS(s) {
    var cssmin = require('gulp-cssmin');

    return s.pipe(cssmin());
}

function copy(stream) {
    return stream;
}

function copyStatic(stream) {
    var filter = ignore.include(/\.(png|jpg|jpeg|gif|svg|ttf|woff|woff2|eot|otf|map|min\.js|min\.css)$/);

    return stream.pipe(filter)
}

function js(stream, babelify) {
    stream = stream.pipe(ignore.include(/\.js$/));
    stream = stream.pipe(ignore.exclude(/\.(min|pack)\.js$/));

    if (babelify) {
        var babel = require('gulp-babel');

        stream = stream.pipe(babel({
            presets: ['es2015']
        }));
    }

    // Minify
    if (!debug)
        stream = minifyJS(stream);

    return stream;
}


function css(stream) {
    stream = stream.pipe(ignore.include(/\.css$/));
    stream = stream.pipe(ignore.exclude(/\.(min|pack)\.css$/));

    // Minify
    if (!debug)
        stream = minifyCSS(stream);

    return stream;
}

function less(stream) {
    var gulpLess = require('gulp-less');

    stream = stream.pipe(ignore.include(/\.less/)).pipe(gulpLess());

    // Minify
    if (!debug)
        stream = minifyCSS(stream);

    return stream;
}


gulp.task('default', function () {
    var tasksFile = yargs.argv.tasksFile;

    if (!tasksFile)
        throw 'Tasks file path is not specified';

    fs.readFile(yargs.argv.tasksFile, 'utf8', function (err, data) {
        if (err) {
            return console.log(err);
        }

        var tasks = JSON.parse(data);
        for (var i = 0; i < tasks.length; i++) {
            var task = tasks[i];
            var stream = gulp.src(task.source);

            switch (task.name) {
                case 'copy':
                    stream = copy(stream);
                    break;

                case 'copy_static':
                    stream = copyStatic(stream);
                    break;

                case 'css':
                    stream = css(stream);
                    break;

                case 'less':
                    stream = less(stream);
                    break;

                case 'js':
                    stream = js(stream);
                    break;

                case 'browserify':
                    stream = browserify(stream);
                    break;

                default:
                    throw 'Unknown task: ' + task.name;
            }

            stream.pipe(gulp.dest(task.destination));
        }
    });
});
