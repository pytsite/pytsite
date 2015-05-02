from pytsite import application, odm


application.run()


class Article(odm.Model):
    def setup(self):
        self.define_field('title', odm.StringField())
        self.define_field('body', odm.StringField())

odm.register_model('article', Article)
# d = odm.dispense('article', '54d477e1fe9c8715678b4579')

d = odm.find('article').sort([('title', 1)]).get(100)
for doc in d:
    print(doc.f_get('title'))


#
# print(d.get('title'))
#
# print(d)