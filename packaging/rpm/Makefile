srpm:
	@VERSION=$$(curl -sf https://api.github.com/repos/WenYin-Community/ZedG/releases/latest \
	  | jq -r '.tag_name' | sed 's/^v//') && \
	echo ">>> Latest version: $$VERSION" && \
	sed "s/%(curl.*\$$/Version:        $$VERSION/" zedg-copr.spec > zedg.spec && \
	rpmbuild -bs zedg.spec
