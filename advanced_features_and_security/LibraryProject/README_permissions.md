إعداد الصلاحيات والمجموعات في المشروع

1) صلاحيات الموديل
   تم تعريف الصلاحيات التالية على الموديل Book في app اسمها bookshelf:
   - can_view
   - can_create
   - can_edit
   - can_delete

   الصلاحيات متاحة كـ codenames تحت app_label=bookshelf:
   أمثلة لاستخدامها: 'bookshelf.can_edit'

2) إضافة المجموعات ومنح الصلاحيات (الطريقة اليدوية عبر Admin)
   - سجل دخولك إلى لوحة الإدارة (/admin/) بمستخدم Superuser.
   - اذهب إلى "Groups" ثم أنشئ المجموعات: Editors, Viewers, Admins.
   - افتح كل مجموعة ثم اختر Permissions المناسبة:
     * Viewers: اختر permission "bookshelf | book | Can view book" فقط.
     * Editors: اختر "Can view book", "Can create book", "Can edit book".
     * Admins: اختر كل الصلاحيات بما فيها "Can delete book" بالإضافة إلى الصلاحيات الأخرى المطلوبة.

3) إضافة المجموعات ومنح الصلاحيات برمجياً (مثال قصير)
   يمكنك تشغيل هذا المقتطف في django shell لتنفيذ الإعداد تلقائياً:
   from django.contrib.auth.models import Group, Permission
   from django.contrib.contenttypes.models import ContentType
   from bookshelf.models import Book
   content_type = ContentType.objects.get_for_model(Book)
   perms = {
       'can_view': Permission.objects.get(content_type=content_type, codename='can_view'),
       'can_create': Permission.objects.get(content_type=content_type, codename='can_create'),
       'can_edit': Permission.objects.get(content_type=content_type, codename='can_edit'),
       'can_delete': Permission.objects.get(content_type=content_type, codename='can_delete'),
   }
   viewers, _ = Group.objects.get_or_create(name='Viewers')
   editors, _ = Group.objects.get_or_create(name='Editors')
   admins, _ = Group.objects.get_or_create(name='Admins')
   viewers.permissions.set([perms['can_view']])
   editors.permissions.set([perms['can_view'], perms['can_create'], perms['can_edit']])
   admins.permissions.set([perms['can_view'], perms['can_create'], perms['can_edit'], perms['can_delete']])

4) التحقق والاختبار
   - أنشئ مستخدمين مختلفين في Admin وأضفهم إلى المجموعات المناسبة.
   - سجّل دخول كل مستخدم وحاول الوصول إلى المسارات:
     * /bookshelf/         -> يتطلب can_view
     * /bookshelf/create/  -> يتطلب can_create
     * /bookshelf/edit/<id>/ -> يتطلب can_edit
     * /bookshelf/delete/<id>/ -> يتطلب can_delete
   - عندما لا يمتلك المستخدم الصلاحية سيُرمى استثناء PermissionDenied (حالة 403).

5) ملاحظات
   - بعد إضافة أو تعديل الصلاحيات في models.py نفّذ:
     python manage.py makemigrations
     python manage.py migrate
   - الصلاحيات تُنشأ في قاعدة البيانات بعد تشغيل الميجريشنات.
