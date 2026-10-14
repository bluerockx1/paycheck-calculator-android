[app]

title = Paycheck Calculator
package.name = paycheckcalculator
package.domain = org.bluerockx1
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

exclude_dirs = .git, .github, bin, .buildozer, __pycache__

[buildozer]
log_level = 2
warn_on_root = 1
