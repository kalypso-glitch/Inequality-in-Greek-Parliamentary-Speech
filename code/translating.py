import argostranslate.package

argostranslate.package.update_package_index()

packages = argostranslate.package.get_available_packages()

package = next(
    p for p in packages
    if p.from_code == "el" and p.to_code == "en"
)

argostranslate.package.install_from_path(package.download())

print("Greek → English installed")