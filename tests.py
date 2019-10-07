from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId


sample_playlist_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_playlist = {
    'title': 'aladdin',
    'description':'Aladdin 2019 Full Movie Subtitle Indonesia aladin 2019 sub indonesia',
    'realse_date': 'May 19, 2019',
    'link':"https://www.youtube.com/embed/jYMP6WUlYoo",
    'image':"https://cdn3-www.comingsoon.net/assets/uploads/2019/07/Aladdin.jpg"

}
sample_form_data = {
    'title': sample_playlist['title'],
    'description': sample_playlist['description'],
    'videos': '\n'.join(sample_playlist['link']),
    'image': '\n'.join(sample_playlist['image'])
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
        self.assertIn(b'MOVIES:))!!', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_playlist(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/movies/{sample_playlist_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'aladdin', result.data)

if __name__ == '__main__':
    unittest_main()
