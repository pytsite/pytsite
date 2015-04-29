from pytsite import application, router, entity, assetman


app = application.Application()

app.register_plugin(assetman.AssetmanPlugin(app))
app.run()