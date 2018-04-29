import unittest
import os
import shutil
from vscodenv import vscode_extensions
from vscodenv import utils

class TestVscodeExtensions(unittest.TestCase):

    def setUp(self):
        # setup fake extensions
        self.extension_to_install = 'cstrap.python-snippets' # lightweight extension
        self.fake_global_extension = 'global.extension-1.5.6'

        self.extensions_dir = "tests/extensions"
        self.installed_extensions = ['author.extension-name-0.3.2', 'author1.extension2-name-1.0.3']
        self.uninstalled_extensions = ['author2.extension4-name-12.0.7', 'authorsdvs2.extensi-name-0.7']
        self.extensions = self.installed_extensions + self.uninstalled_extensions
        self.invalid_folder_extensions = ["author1.extension10-name-2.0.7"] # there is no package.json
        self.file_extensions = ["thor1.extesion10-nam-2.0"] # the extension is a file not a folder
        
        os.mkdir(self.extensions_dir)

        ext_dir = os.path.join(utils.get_global_extensions_dir(), self.fake_global_extension)
        os.mkdir(ext_dir)
        package_json_path = os.path.join(ext_dir, "package.json")
        f = open(package_json_path, 'w+')
        f.close()

        for ext in self.file_extensions:
            ext_dir = os.path.join(self.extensions_dir, ext)
            f = open(ext_dir, 'w+')
            f.close()

        for ext in self.invalid_folder_extensions:
            ext_dir = os.path.join(self.extensions_dir, ext)
            os.mkdir(ext_dir)

        for ext in self.extensions:
            ext_dir = os.path.join(self.extensions_dir, ext)
            os.mkdir(ext_dir)
            package_json_path = os.path.join(ext_dir, "package.json")
            f = open(package_json_path, 'w+')
            f.close()

        # generate .obsolete file
        dot_obsolete_path = os.path.join(self.extensions_dir, '.obsolete')
        dot_obsolete_content = '{'
        for ext in self.uninstalled_extensions:
            dot_obsolete_content += '"%s": true,' % ext
        dot_obsolete_content = dot_obsolete_content[:-1]
        dot_obsolete_content += '}'

        with open(dot_obsolete_path, 'w+') as f:
            f.write(dot_obsolete_content)

    # get_extensions
    def test_get_extensions_should_return_installed_extensions(self):
        ret = vscode_extensions.get_extensions(self.extensions_dir)
        self.assertCountEqual(ret, self.installed_extensions)

    def test_get_extensions_should_return_empty_if_extensions_dir_not_exists(self):
        fake_path = "path_that_does_not_exist"
        ret = vscode_extensions.get_extensions(fake_path)
        self.assertEqual(ret, [])

    # get_uninstalled_extensions
    def test_get_uninstalled_extensions(self):
        ret = vscode_extensions.get_uninstalled_extensions(self.extensions_dir)
        self.assertCountEqual(ret, self.uninstalled_extensions)

    def test_get_uninstalled_extensions_should_return_empty_if_dot_obsolete_not_exists(self):
        fake_path = "path_that_does_not_exist"
        ret = vscode_extensions.get_uninstalled_extensions(fake_path)
        self.assertEqual(ret, [])

    # remove_extension_from_uninstalled
    def test_remove_extension_from_uninstalled_should_remove_extension_from_dot_obsolete(self):
        ext_base_name = utils.extension_base_name(self.uninstalled_extensions[0])
        vscode_extensions.remove_extension_from_uninstalled(ext_base_name, self.extensions_dir)
        ret = vscode_extensions.get_uninstalled_extensions(self.extensions_dir)
        true_uninstalled_extensions = self.uninstalled_extensions[1:]

        self.assertCountEqual(ret, true_uninstalled_extensions)

    # install_extension
    def test_install_extension_should_install_extension_if_not_installed(self):
        vscode_extensions.install_extension(self.extension_to_install, self.extensions_dir)
        installed_extensions = vscode_extensions.get_extensions(self.extensions_dir)
        self.assertTrue(self.extension_to_install in [utils.extension_base_name(ext) for ext in installed_extensions])

    def test_install_extension_should_create_symlink_if_installed_global(self):
        vscode_extensions.install_extension(utils.extension_base_name(self.fake_global_extension), self.extensions_dir)
        ext_is_symlink = os.path.islink(os.path.join(self.extensions_dir, self.fake_global_extension))
        self.assertTrue(ext_is_symlink)

    # def test_install_extension_should_remove_from_uninstalled_if_uninstalled(self):

    def tearDown(self):
        shutil.rmtree(self.extensions_dir)
        shutil.rmtree(os.path.join(utils.get_global_extensions_dir(), self.fake_global_extension))

if __name__ == '__main__':
    unittest.main()