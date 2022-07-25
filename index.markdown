---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

# Download your home

```shell
d=$(date +%Y-%m-%d)
echo "$d"
```

```shell
cd $ZREPO/_posts
wget -O $d-home.md https://raw.githubusercontent.com/bamr87/it-journey/master/home.md 
```
