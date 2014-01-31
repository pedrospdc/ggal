from tempfile import mkdtemp
from django.core.files.base import File
from django.test.utils import override_settings
import os

from django.test import TestCase
from django.test.client import RequestFactory, Client

from core.models import Picture
from core.views import PictureCreate, PictureUpdate
from gal.settings import ASSETS_ROOT

tmp_dir = mkdtemp()
test_file_path = os.path.join(ASSETS_ROOT, 'mergepls.jpg')


@override_settings(MEDIA_ROOT=tmp_dir)
class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.factory = RequestFactory()


class PictureCreateTestCase(BaseTestCase):
    def setUp(self):
        super(PictureCreateTestCase, self).setUp()
        self.view = PictureCreate.as_view()
        self.url = '/picture/create'

    def test_ensure_create_picture_page_can_be_accessed(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_ensure_create_picture_post_creates_an_picture(self):
        file_path = os.path.join(ASSETS_ROOT, 'mergepls.jpg')

        with open(file_path) as f:
            request = self.factory.post(self.url, {'title': 'Pls', 'file': f})

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        picture = Picture.objects.first()
        self.assertEqual(os.path.basename(file_path), os.path.basename(picture.file.url))

    def test_ensure_picture_upload_is_mandatory(self):
        request = self.factory.post(self.url, {'title': 'Pls'})
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_ensure_title_is_not_required(self):
        with open(test_file_path) as f:
            request = self.factory.post(self.url, {'file': f})

        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        picture = Picture.objects.first()
        self.assertEqual('', picture.title)


class PictureUploadTestCase(BaseTestCase):
    def setUp(self):
        super(PictureUploadTestCase, self).setUp()
        self.view = PictureUpdate.as_view()

        with open(test_file_path) as f:
            file_ = File(f)
            self.picture = Picture.objects.create(title='Cat', file=file_)

        self.url = '/picture/edit'

    def test_ensure_update_picture_page_can_be_accessed(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.picture.pk)
        self.assertEqual(response.status_code, 200)
    
    def test_ensure_update_picture_will_update_picture_data(self):
        file_path = os.path.join(ASSETS_ROOT, 'koala.jpg')

        with open(file_path) as f:
            request = self.factory.post(self.url, {'file': f, 'title': 'Koala'})

        response = self.view(request, pk=self.picture.pk)
        self.assertEqual(response.status_code, 302)

        picture = Picture.objects.first()

        self.assertEqual(os.path.basename(file_path), os.path.basename(picture.file.url))
        self.assertEqual('Koala', picture.title)
        self.assertEqual(1, Picture.objects.count())


class PictureListTestCase(BaseTestCase):
    def setUp(self):
        super(PictureListTestCase, self).setUp()
        self.view = PictureCreate.as_view()
        with open(test_file_path) as f:
            file_ = File(f)
            for i in range(3):
                self.picture = Picture.objects.create(title='Cat %d' % i, file=file_)

        self.url = '/picture/list/'
        self.template = 'core/picture_list.html'

    def test_ensure_picture_list_page_can_be_accessed(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(list(Picture.objects.all()), list(response.context['object_list']))


class GalleryTestCase(PictureListTestCase):
    def setUp(self):
        # As the gallery stands for the same page as picturelist, we'll just change the context used
        self.url = '/'
        self.template = 'core/gallery.html'