# Maintainer: Your Name <your.email@example.com>
pkgname=nbfc-qt-git
pkgver=0.1.0
pkgrel=1
pkgdesc="A GUI for Notebook FanControl"
arch=('x86_64')
url="https://github.com/TiagoRibeiro25/nbfc-qt"
license=('GPL')
depends=('python' 'python-pyqt6' 'nbfc-linux')
makedepends=('git' 'python-setuptools')
source=('git+https://github.com/TiagoRibeiro25/nbfc-qt.git')
sha256sums=('SKIP')

pkgver() {
    cd "$srcdir/nbfc-qt"
    git describe --tags | sed 's/^v//;s/-/+/g'
}

package() {
    cd "$srcdir/nbfc-qt"

    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt

    # Create the target directories
    mkdir -p "$pkgdir/usr/share/nbfc-qt"
    mkdir -p "$pkgdir/usr/bin"  # Ensure /usr/bin exists

    # Install your application
    cp -r . "$pkgdir/usr/share/nbfc-qt"
    
    # Create a symbolic link for the main executable
    ln -s "/usr/share/nbfc-qt/main.py" "$pkgdir/usr/bin/nbfc-qt"

    # Deactivate the virtual environment
    deactivate
}

