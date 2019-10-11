from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId


sample_movie_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_movie = {
    'title': 'aladdin',
    'description':'Aladdin 2019 Full Movie Subtitle Indonesia aladin 2019 sub indonesia',
    'link':"https://www.youtube.com/embed/jYMP6WUlYoo",
    'image':"https://cdn3-www.comingsoon.net/assets/uploads/2019/07/Aladdin.jpg"

}

sample_movie_update = {
    'title': 'aladdin',
    'description':'Aladdin 2019 Full Movie Subtitle Indonesia aladin 2019 sub indonesia'
}

sample_form_data = {
    'title': sample_movie['title'],
    'description': sample_movie['description'],
    'link': '\n'.join(sample_movie['link']),
    'image': (sample_movie['image'])
}

class MoviesTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the movies homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    def test_register(self):
        """Test the regestration page."""
        result = self.client.get('/register')
        self.assertEqual(result.status, '200 OK')

    def test_login(self):
        """Test the regestration page."""
        result = self.client.get('/login')
        self.assertEqual(result.status, '200 OK')

    def movies_index(self):
        """Test the regestration page."""
        result = self.client.get('/movies')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_movie(self, mock_find):
        """Test showing a single movie."""
        mock_find.return_value = sample_movie

        result = self.client.get(f'/movies/{sample_movie_id}')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_movie(self, mock_find):
        """Test editing a single movie."""
        mock_find.return_value = sample_movie

        result = self.client.get(f'/movies/{sample_movie_id}/edit')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_movie(self, mock_update):
        result = self.client.post(f'/movies/{sample_movie_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_movie_id}, {'$set': sample_movie_update})

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_delete_movie(self, mock_find):
        """Test deleting a single movie."""
        mock_find.return_value = sample_movie
        result = self.client.get('/movies')
        self.assertEqual(result.status, '200 OK')

    # @mock.patch('pymongo.collection.Collection.find_one')
    # def test_edit_delete(self, mock_find):
    #     """Test deleting a single movie."""
    #     mock_find.return_value = sample_movie
    #     result = self.client.get(f'/movies/{sample_movie_id}/delete')
    #     self.assertEqual(result.status, '200 OK')
# /movies/<movie_id>/delete
if __name__ == '__main__':
    unittest_main()
