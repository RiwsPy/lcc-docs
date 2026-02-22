from models.url import HttpUrl


class TestUrl:
    def test_basic_url(self):
        url = "https://toto.com/"
        expected_value = url

        assert HttpUrl(url).url == expected_value

    def test_url_without_slash(self):
        url = "https://toto.com"
        expected_value = url + "/"

        assert HttpUrl(url).url == expected_value

    def test_is_direct_archive(self):
        url = "https://toto.com/"
        expected_value = False

        assert HttpUrl(url).is_direct_archive is expected_value

    def test_is_direct_archive_true(self):
        url = "https://toto.com/file.exe"
        expected_value = True

        assert HttpUrl(url).is_direct_archive is expected_value

    def test_is_direct_archive_true_case(self):
        url = "https://toto.com/file.eXE"
        expected_value = True

        assert HttpUrl(url).is_direct_archive is expected_value

    def test_is_direct_archive_sorcerers(self):
        url = "https://sorcerers.net/file.exe"
        expected_value = False

        assert HttpUrl(url).is_direct_archive is expected_value

    def test_tld(self):
        url = "https://toto.com"
        expected_value = "com"

        assert HttpUrl(url).tld == expected_value

    def test_is_external(self):
        url = "https://toto.com/"
        expected_value = True

        assert HttpUrl(url).is_external is expected_value

    def test_image_domain(self, mocker):
        mocker.patch.object(HttpUrl, "domain_to_image", {"toto.com": "image-toto.avif"})

        url = "https://toto.com/"
        expected_value = "image-toto.avif"

        assert HttpUrl(url)._image_domain() == expected_value

    def test_image_domain_not_found(self, mocker):
        mocker.patch.object(HttpUrl, "domain_to_image", dict())

        url = "https://toto.com/"
        expected_value = ""

        assert HttpUrl(url)._image_domain() == expected_value

    def test_image_subdomain(self, mocker):
        mocker.patch.object(HttpUrl, "domain_to_image", {"toto.com": "image-toto.avif"})

        url = "https://sub.toto.com/"
        expected_value = "image-toto.avif"

        assert HttpUrl(url)._image_domain() == expected_value

    # TODO url.image
