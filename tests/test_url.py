from models.url import HttpUrl
from scripts.utils import minify_url


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

    def test_is_direct_archive_github(self):
        url = "https://github.com/toto/mod/raw/refs/file.exe"
        expected_value = True

        assert HttpUrl(url).is_direct_archive is expected_value

        url = "https://github.com/toto/mod/blob/main/file.exe"
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


class Test_minify_url:
    def test_www(self):
        url = "https://www.toto.com"
        expected_value = "https://toto.com"

        assert minify_url(url) == expected_value

    def test_dash_end(self):
        url = "https://toto.com/"
        expected_value = "https://toto.com"

        assert minify_url(url) == expected_value

    def test_baldur_de(self):
        url = "https://baldurs-gate.de/index.php?threads/toto.5094"
        expected_value = "https://baldurs-gate.de/index.php?threads/5094"

        assert minify_url(url) == expected_value

    def test_gibberlings_topic(self):
        url = "https://gibberlings3.net/forums/topic/5094-toto"
        expected_value = "https://gibberlings3.net/forums/topic/5094-l"

        assert minify_url(url) == expected_value

    def test_gibberlings_file(self):
        url = "https://gibberlings3.net/files/file/5094-toto"
        expected_value = "https://gibberlings3.net/files/file/5094-l"

        assert minify_url(url) == expected_value

    def test_shs_topic(self):
        url = "https://shsforums.net/topic/5094-toto"
        expected_value = "https://shsforums.net/topic/5094-l"

        assert minify_url(url) == expected_value

    def test_shs_forum(self):
        url = "https://shsforums.net/forum/5094-toto"
        expected_value = "https://shsforums.net/forum/5094-l"

        assert minify_url(url) == expected_value

    def test_beamdog(self):
        url = "https://forums.beamdog.com/discussion/50975/toto"
        expected_value = "https://forums.beamdog.com/discussion/50975"

        assert minify_url(url) == expected_value

    def test_github(self):
        url = "https://github.com/Toto/TotoRepo/blob/main/file.txt"
        expected_value = "https://github.com/Toto/TotoRepo"

        assert minify_url(url) == expected_value

    def test_github_raw_protected(self):
        url = "https://github.com/Toto/TotoRepo/raw/refs/heads/main/mod.zip"
        expected_value = url

        assert minify_url(url) == expected_value

    def test_github_releases_protected(self):
        url = "https://github.com/Toto/TotoRepo/releases/download/mod.zip"
        expected_value = url

        assert minify_url(url) == expected_value
