"""
Check for required dependencies and minimum versions
"""
import sys
import pkg_resources
import importlib

def check_dependencies():
    """Check for required dependencies and versions"""
    # Minimum required Python version
    required_python_version = (3, 7)
    if sys.version_info < required_python_version:
        print(f"Error: Python {required_python_version[0]}.{required_python_version[1]} or higher is required")
        print(f"Your Python version: {sys.version}")
        return False
    
    # Required packages and minimum versions
    requirements = {
        "pygame": "2.0.0"
    }
    
    missing_packages = []
    outdated_packages = []
    
    for package, min_version in requirements.items():
        try:
            # Try to import the package
            importlib.import_module(package)
            
            # Check version
            installed_version = pkg_resources.get_distribution(package).version
            
            # Compare versions
            if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(min_version):
                outdated_packages.append((package, installed_version, min_version))
            
        except (ImportError, pkg_resources.DistributionNotFound):
            missing_packages.append((package, min_version))
    
    # Print status
    if not missing_packages and not outdated_packages:
        print("All dependencies are satisfied!")
        return True
    
    # Report problems
    if missing_packages:
        print("Missing required packages:")
        for package, version in missing_packages:
            print(f"  - {package} (>= {version})")
    
    if outdated_packages:
        print("Outdated packages:")
        for package, installed, required in outdated_packages:
            print(f"  - {package}: {installed} installed, but {required} required")
    
    # Suggest installation command
    print("\nYou can install required packages using:")
    packages = [f"{p}>={v}" for p, v in missing_packages]
    packages.extend([f"{p}>={r}" for p, i, r in outdated_packages])
    
    if packages:
        print(f"pip install {' '.join(packages)}")
    
    return False

if __name__ == "__main__":
    check_dependencies()
