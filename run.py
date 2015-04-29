from pytsite import app, router, entity


app.register_plugin(entity.EntityPlugin)
app.run()