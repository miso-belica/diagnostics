document.body.addEventListener("click", function(evt) {
	// find source element
	var target = evt.target
	if(!target || !target.tagName) {
		return true
	}

	var tagName = target.tagName.toLowerCase(),
		handled = false,
		tag = null
	if(tag = findParentTag(target, "a")) {
		handled = handleAnchor(tag)
	}
	else if(tag = findParentTag(target, "li")) {
		handled = handleListItem(tag)
	}

	if(handled) {
		evt.preventDefault()
		return false
	}
	else {
		return true
	}
}, false)


function findParentTag(tag, tagName) {
	do {
		if(tag.tagName && tag.tagName.toLowerCase() === tagName) {
			return tag
		}

		tag = tag.parentNode
	} while(tag)

	return null
}


function handleAnchor(target) {
	var href = target.getAttribute("href")
	if(!href || href.charAt(0) !== "#") {
		return false
	}

	var targetPanel = document.getElementById(href.slice(1)),
		panelFolded = targetPanel.classList.toggle("folded"),
		abbrevation = target.getElementsByTagName("abbr")[0]

	if(abbrevation) {
		abbrevation.innerHTML = panelFolded ? "▶" : "▼"
	}

	return true
}


function handleListItem(target) {
	if(!target.dataset.targetPanel) {
		return false
	}

	var listItems = target.parentNode.getElementsByTagName("li"),
		targetPanel = document.getElementById(target.dataset.targetPanel),
		itemsDisplayed = !targetPanel.classList.toggle("folded")

	for(var i = 0; i < listItems.length; ++i) {
		if(listItems[i] === target) {
			target.parentNode.start += itemsDisplayed ? -i : i
			break
		}
	}

	return true
}
