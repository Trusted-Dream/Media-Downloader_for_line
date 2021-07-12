from line.downloader import Worker
class TestUpload(object):
    def setup_method(self):
        self.url = "https://www.youtube.com/watch?v=4pqJA7aiVJc"
        self.tag = "/mp3"

    def test_upload(self):
        try:
            Worker(self.tag,self.url,None,None).run()
            assert True
        except Exception:
            assert False

    def test_invalid_url(self):
        # Invalid URL
        self.url = "https://www.youtube.com/"
        try:
            Worker(self.tag,self.url,None,None).run()
            assert False
        except Exception:
            assert True