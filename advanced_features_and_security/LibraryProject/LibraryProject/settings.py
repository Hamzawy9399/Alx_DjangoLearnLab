from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'replace-me-in-production')

# DEBUG يجب أن يكون False في بيئة الإنتاج لعرض أخطاء أقل ومنع تسريب معلومات حساسة
DEBUG = False

# ضع هنا نطاقات موقعك الفعلية (مث: 'example.com')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'relationship_app',
    'accounts',
    'books',
    'library',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bookshelf.middleware.SecurityHeadersMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'bookshelf.CustomUser'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# -------------------------------------------------------------------
# Security-related settings (HTTPS and headers)
# -------------------------------------------------------------------

# عندما يكون True سيعيد Django توجيه أي طلب HTTP إلى HTTPS.
# يجب تفعيل هذا بعد تثبيت شهادة SSL على مستوى الويب سيرفر (Nginx/Apache).
SECURE_SSL_REDIRECT = True

# HSTS: يخبر المتصفح أن يستخدم HTTPS فقط لهذا النطاق لعدد الثواني المحدد.
# القيمة 31536000 تكافئ سنة واحدة. فعلها فقط عندما تكون متأكدًا من أن HTTPS يعمل تمامًا.
SECURE_HSTS_SECONDS = 31536000

# تضمين جميع النطاقات الفرعية في سياسة HSTS (شغّلها فقط إذا تغطّي الشهادة كل النطاقات الفرعية أو ترغب في ذلك).
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# يسمح بطلب إضافة الموقع إلى preload list الخاصة بالمتصفحات
SECURE_HSTS_PRELOAD = True

# منع إرسال ملفات تعريف الارتباط (session/csrf) عبر اتصالات غير مشفرة.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# يمنع المتصفح من محاولة "MIME sniffing" لمحتوى الاستجابة (حماية ضد بعض أنواع الهجوم).
SECURE_CONTENT_TYPE_NOSNIFF = True

# يطلب من المتصفح محاولة تمكين فلتر XSS
SECURE_BROWSER_XSS_FILTER = True

# يمنع تضمين الموقع داخل إطارات على مواقع أخرى (حماية من clickjacking)
X_FRAME_OPTIONS = 'DENY'

# إذا كان التطبيق خلف بروكسي/Load Balancer يرسل HTTP_X_FORWARDED_PROTO = 'https'
# يجب تعريف هذا حتى يعتبر Django الطلب مؤمناً. تأكد من ضبط البروكسي لتمرير العنوان.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# عدد مرات تجربة إعادة التوجيه عند استخدام SECURE_SSL_REDIRECT في الحالات الخاصة
# (يمكن تركه افتراضيًا؛ لا حاجة لتعديله عادة)
# SECURE_REFERRER_POLICY = 'same-origin'  # مثال إن رغبت بتقييد الريفيرر

# Content Security Policy: يُنصح بتثبيت django-csp وضبط السياسات بدقة.
# المشروع يحتوي على middleware يقوم بإضافة CSP أساسي. في الإنتاج قد ترغب بسياسة أكثر تحديداً.
# مثال: CSP_DEFAULT_SRC = ("'self'",)

# تذكير أمني عملي:
# - احفظ SECRET_KEY وقيم حساسة أخرى في متغيرات بيئة (ENV) أو نظام سرّي، لا تضعها في المستودع.
# - تأكد من أن ALLOWED_HOSTS يحتوي على أسماء النطاق الفعلية قبل تفعيل في الإنتاج.
