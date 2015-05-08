from ..core import router, tpl, assetman

router.add_rule('/admin', __name__ + '.views@dashboard')
tpl.register_package(__name__)
assetman.register_package(__name__)
