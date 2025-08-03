#!/usr/bin/env python3
"""
Portfolio Deployment Verification Script
Run this script to verify your Render deployment is working correctly.
"""

import requests
import time
from urllib.parse import urljoin

# Your deployment URL
SITE_URL = "https://portfolio-56yz.onrender.com/"

def test_site_accessibility():
    """Test if the main site is accessible"""
    print("🔍 Testing Site Accessibility...")
    print("-" * 50)
    
    try:
        response = requests.get(SITE_URL, timeout=30)
        print(f"✅ Site Status: {response.status_code}")
        print(f"✅ Response Time: {response.elapsed.total_seconds():.2f}s")
        print(f"✅ Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Site is accessible!")
            return True
        else:
            print(f"❌ Site returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot reach the site")
        print("   This could mean:")
        print("   - Site is not deployed yet")
        print("   - URL is incorrect")
        print("   - Network connectivity issue")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: Site is taking too long to respond")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_static_assets():
    """Test if static assets are loading correctly"""
    print("\n🎨 Testing Static Assets...")
    print("-" * 50)
    
    static_files = [
        "/static/css/styles.css",
        "/static/js/main.js"
    ]
    
    results = []
    for asset in static_files:
        try:
            url = urljoin(SITE_URL, asset)
            response = requests.head(url, timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {asset}: {response.status_code}")
            results.append(response.status_code == 200)
        except Exception as e:
            print(f"❌ {asset}: Error - {str(e)}")
            results.append(False)
    
    return all(results)

def test_key_pages():
    """Test if key pages are accessible"""
    print("\n📄 Testing Key Pages...")
    print("-" * 50)
    
    pages = [
        "/",
        "/about/",
        "/projects/",
        "/contact/",
        "/admin/"
    ]
    
    results = []
    for page in pages:
        try:
            url = urljoin(SITE_URL, page)
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code in [200, 302, 403] else "❌"
            print(f"{status} {page}: {response.status_code}")
            results.append(response.status_code in [200, 302, 403])
        except Exception as e:
            print(f"❌ {page}: Error - {str(e)}")
            results.append(False)
    
    return all(results)

def check_cloudinary_integration():
    """Check if Cloudinary is properly integrated"""
    print("\n☁️ Testing Cloudinary Integration...")
    print("-" * 50)
    
    try:
        response = requests.get(SITE_URL, timeout=10)
        content = response.text
        
        if "res.cloudinary.com" in content:
            print("✅ Cloudinary URLs found in page content")
            return True
        else:
            print("❌ No Cloudinary URLs found - check media file configuration")
            return False
    except Exception as e:
        print(f"❌ Error checking Cloudinary: {str(e)}")
        return False

def check_security_headers():
    """Check if security headers are present"""
    print("\n🔒 Testing Security Headers...")
    print("-" * 50)
    
    try:
        response = requests.get(SITE_URL, timeout=10)
        headers = response.headers
        
        security_checks = {
            "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
            "X-Frame-Options": headers.get("X-Frame-Options"),
            "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
            "Content-Security-Policy": headers.get("Content-Security-Policy")
        }
        
        for header, value in security_checks.items():
            status = "✅" if value else "⚠️"
            print(f"{status} {header}: {value or 'Not Set'}")
            
    except Exception as e:
        print(f"❌ Error checking security headers: {str(e)}")

def main():
    """Run all verification tests"""
    print("🚀 Portfolio Deployment Verification")
    print("=" * 60)
    print(f"Testing URL: {SITE_URL}")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Site Accessibility", test_site_accessibility),
        ("Static Assets", test_static_assets),
        ("Key Pages", test_key_pages),
        ("Cloudinary Integration", check_cloudinary_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Security headers (informational)
    check_security_headers()
    
    # Summary
    print("\n📊 Verification Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nScore: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your deployment is working correctly.")
        print("\n✅ Next Steps:")
        print("   1. Test the site manually in your browser")
        print("   2. Check Render logs for any errors")
        print("   3. Test contact form functionality")
        print("   4. Verify dashboard login works")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Check Render dashboard for deployment status")
        print("   2. Verify environment variables are set correctly")
        print("   3. Check application logs for errors")
        print("   4. Ensure the service is fully deployed and running")

if __name__ == "__main__":
    main()
