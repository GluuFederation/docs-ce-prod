

/* ----------------------------------------------------------------------------
 * Taken and adapted from https://gist.github.com/kylebarrow/1042026
 * ------------------------------------------------------------------------- */

/* Detect standalone mode */
if (('standalone' in window.navigator) && window.navigator.standalone) {

	/* If you want to prevent remote links in standalone web apps opening
	   Mobile Safari, change 'remotes' to true */
	var node, remotes = false;

	/* Bind to document */
	document.addEventListener('click', function(event) {
		node = event.target;

		/* Bubble up until we hit link or top HTML element. Warning: BODY element
		   is not compulsory so better to stop on HTML */
		while (node.nodeName !== 'A' && node.nodeName !== 'HTML') {
			node = node.parentNode;
	  }
		if ('href' in node && node.href.indexOf('http') !== -1 && (
				node.href.indexOf(document.location.host) !== -1 || remotes)) {
			event.preventDefault();
			document.location.href = node.href;
		}
	}, false);
}