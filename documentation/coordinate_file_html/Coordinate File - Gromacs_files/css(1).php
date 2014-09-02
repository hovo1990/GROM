/* 
	_style.css (11,313), 
	_content.css (3,837)
 */

/* --------- _STYLE.CSS --------- */

body {
	padding:20px;	
	font-size:12px;
	background-position: top center;
	background-repeat: repeat-x;
	background-color:#e9e9cf;
}
.global {
	background-color:#fff;
	padding:0;
	border:2px solid #fff;
	-moz-border-radius:10px;
	width:expression(document.body.clientWidth < 800 ? "800px" : "auto" );
	background-image:url(images/global_bg.gif);
	background-repeat:repeat-y;
	overflow:hidden;
}
.content-frame {
	padding:10px;	
	background-color:#fff;
}
.flex-logo {
	width:217px;
	background-image:url(images/flex_waves.png);	
	background-position:bottom right;
	background-repeat:no-repeat;
}
.upload-logo:visited,
.upload-logo {
	font-size:10px;
	display:block;
	text-align:center;
	margin:0 10px;
	padding:2px;
	min-height:0;	
	color:#fff;
	-moz-border-radius:3px;
	margin-bottom:2px;
}
.upload-logo:hover {
	background-image:url(images/white-transparent.png);
}
.color-pick {
	display:block;
	float:right;
	border:1px solid #fff;
	height:10px;
	margin:5px 5px 0 0;
	width:10px;
	font-size:0;
	cursor:pointer;
}
/*META DATA*/
.page-meta-data {
	clear:both;
	border-top:1px solid #efefef;
	background-repeat:repeat-x;
	padding:0;
	margin:0 0 20px 0;
	display:block;
}

.page-meta-data h3 {
	border:0;
	font-size:20px;
	color:#333;
	
}
.meta-link {
	float:right;
	padding-top:5px;	
}
/*Position CSS*/
.br {
	clear:both;	
}
.fr {
	float:right;	
}
.first {
	margin-left:0 !important;
	margin-top:0 !important;	
}
.last {
	margin-bottom:0 !important;	
}
/*TITLE AND HEADER*/
.header-sub {
	color:#999;
	padding-left:10px;
}
.page-restricted {
	padding-left:20px;
	background:left center url(images/icon-key.gif) no-repeat;
}
/*PAGE ALERTS & PAGE RANKING*/
.page-nav .right-bar {
	float:right;	
}
#deki-page-alerts,
#deki-page-rating-bar {
	float:right;
	margin:0;
	border:0;
	padding:5px 10px;
	font-size:11px;
	border-right:1px dotted #d2d2d2;
}
#deki-page-rating-bar  {
	border:0;	
}
#deki-page-alerts div.toggle {
	padding:0;
	border:0;
	background:none;	
}
#deki-page-alerts li {
	float:none;	
}
#deki-page-alerts form {
	font-size:11px;
	padding:3px;
	-moz-border-radius:3px;	
}
/*SITE HEAD*/
.site-head {
	min-height:30px;
	background-color:#3383bd;	
	-moz-border-radius-topright:10px;
	-moz-border-radius-topleft:10px;
	background-image:url(images/grad_white.png);
	background-repeat:repeat-x;
	overflow:visible;
	position:relative;
	min-width:800px;
}
.site-head table {
	width:100%;	
}
.site-head table,
.site-head tr,
.site-head td {
	padding:0;
	border:0;	
}
.site-head td {
	padding:0;
	border:0;
}

/*SITE MAST*/
.site-mast {
	width:190px;
	background-image:url(images/white-transparent.png);
}
.site-mast a {
	display:block;
	text-align:center;	
}
.site-mast a.logo-admin {
	display:block;
	text-align:center;	
	padding:5px 0;
}
.site-mast a.logo-anonymous {
	display:block;
	text-align:center;	
	padding:5px 0;
}
/*SITE AUTH*/
.site-auth {
	padding:10px;
	overflow:hidden;
	background-color:#d8ddcf;
	-moz-border-radius-bottomleft:10px;
	height:100%;
}
.site-auth .user-login,
.site-auth .user-name {
	float:left;
}
.site-auth .user-name a {
	font-weight:bold;
}
.site-auth .user-register,
.site-auth .user-logout {
	float:right;
}

.site-auth a:visited,
.site-auth a {
	color:#333;	
}
/*SITE SIDE*/
.site-side {
	background-color:#f3f3e7;
	width:190px;
	vertical-align:top;
}
/*SITE CONTENTS*/
.content-table {
	border:0;
	padding:0;
	margin:0;	
	width:100%;
}
.content-frame {
	overflow:hidden;
	height:100%;
}
.site-side {
	width:190px;
	padding:0;
	margin:0;
	border:0;
}
.site-content {
	padding:0;
	margin:0;
	border:0;
	margin-left:190px;
	min-width:600px;
	vertical-align:top;
}
/*SITE NAVIGATION*/
td.site-nav {
	vertical-align:bottom !important;
	padding:0 0 5px 25px;
}
.site-nav ul {
	margin:0;
	padding:0;
}
.site-nav li {
	float:left;
	list-style-type:none;
	padding:0 3px;
}

.site-nav span,
.site-nav a:visited,
.site-nav a {
	font-size:12px;
	display:block;
	-moz-border-radius:3px;
	padding:5px 5px 5px 5px;
	color:#fff;
}
.site-nav span:hover,
.site-nav a:hover {
	text-decoration:none;
	background-color:#7aaed4;
	cursor:pointer;
	color:#fff;
}

/*PAGE NAVIGATION*/
.page-nav {
	padding:5px 0;
	overflow:hidden;
	background-color:#efefef;
	-moz-border-radius-bottomright:10px;
}
.page-nav ul {
	margin:0 20px;
	padding:0;
	overflow:hidden;	
}
.page-nav li {
	float:left;
	list-style-type:none;
	padding:0 5px;
}
.page-nav li span.a,
.page-nav li a {
	display:block;
	color:#666;
	padding:5px 5px;
	-moz-border-radius:3px;
	text-decoration:none;	
}
.page-nav li span.a:hover,
.page-nav li a:hover {
	cursor:pointer;
	background-color:#d4d4d4;
}

/*PAGE NAVIGATION OPTIONS*/

/*LEFT NAVIGATION*/
#siteNavTree {
	margin-top:20px;
}
#siteNavTree a {
	width:auto !important;	
	font-size:12px;
	display:block !important;
	color:#333;
}
#siteNavTree div.childNode, 
#siteNavTree div.selectedChild {
	
}
#siteNavTree div.sibling, 
#siteNavTree div.dockedNode {
	
}
#siteNavTree a:hover {
	color:#619fcc;
}
#siteNavTree div.homeNode {
	background:none;
	font-weight:bold;
}	
/*PAGE TITLE*/
.pageTitle {
	border-bottom:1px solid #E6E6E6;
}
/*BREADCRUMBS*/
.dw-hierarchy {
	font-size:11px;
	margin:5px 0 10px 0 ;
	display:block;
}
/*POWERED BY MINDTOUCH*/
.powered-by {
	padding:10px 0;
	text-align:center;
}
.powered-by a:visited,
.powered-by a {
	color:#333;	
}
/*SUCCESS / ERROR MESSAGE*/
.upgrade,
.successmsg,
.errormsg,
.systemmsg,
.contentUndelete {
	border:1px solid #f8f0a9;	
	padding:5px;
	background-color:#fefbe1;
	margin:5px 0;
}
/*PAGINATION*/
.deki-pagination {
	padding:5px 0;
	overflow:hidden;
}
.deki-pagination div {
	padding:0;
	margin:0;
	float:left;
	color:#999;
	font-size:11px;
}
.deki-pagination div.prev {
	width:20%;
}
.deki-pagination div.info {
	width:60%;
	text-align:center;
}
.deki-pagination .next {
	width:20%;
	text-align:right;
}
/*SEARCH RESULTS*/
#searchResults {
	margin:10px 0;	
}
#searchResults .searchResults {
	margin:0 0 20px 0;
	font-weight:bold;	
}
#searchResults ul {
	margin:0;
	padding:0;
}
#searchResults li {
	margin:10px 0 ;	
	list-style-type:none;
	border-top:1px dotted #ccc;
	padding:5px 0;
}
#searchResults .icon {
	vertical-align:bottom;	
}
#searchResults li a {
	font-weight:bold;	
}
.deki-parsed-query {
	padding:5px;
	background:#f5f5f5;	
	border:1px solid #efefef;
	-moz-border-radius:3px;
}
/* -- search*/
.site-search {
	padding:0 5px;	
	margin:10px 0 0 0;
}
.site-search select,
.site-search .text {
	width:110px;
	font-size:11px;
	padding:5px;
	border:1px solid #ccc;
	-moz-border-radius:5px;
	margin:0 0 5px 0;
}
.site-search .button {
	font-size:11px;
}
/* -- subnav*/
.deki-page-subnav {
	background:#efefef;
	padding:5px;
	-moz-border-radius:3px;
	margin:5px 0 5px 0;	
	overflow:hidden;
}
.deki-page-subnav ul,
.deki-page-subnav ul li {
	display:inline;
	padding:0;
}
.deki-user-autocomplete {
	background:#efefef;
	border:0;
	-moz-border-radius:5px;	
	padding:5px;
}
.deki-user-autocomplete table,  
.deki-user-autocomplete table td {
	border:0;
}
.deki-rclanguages {
	float:right;	
}
.deki-rc-feeds {
	float:none;
	padding:3px;	
}
.deki-feedlist a {
	margin-left:10px;	
}
/*DROPDOWN CSS*/
.page-nav .drop-arrow span.a,
.site-nav .drop-arrow span.a {
	padding-right:20px;	
	background-image: url(images/drop_grey.gif) !important;
	background-repeat:no-repeat;
	background-position:right 13px;
	cursor:pointer;
	-moz-border-radius-bottomleft:3px;
	-moz-border-radius-bottomright:3px;
}
.site-nav .drop-arrow span.a {
	background-position:right 13px;
}
.page-nav .drop-down,
.site-nav .drop-down {
	display:none;	
	position:absolute;
	background:#e4ebee;
	z-index:10;
	border:1px solid #bbc7cf;
	border-top:0;
	margin:5px 0 0 0;
	padding:5px;
	z-index:10;
}
.page-nav .drop-down li,
.site-nav .drop-down li {
	margin:0;
	padding:0;
	float:none;
	display:block;
	border-bottom:1px solid #b4cbd5;
}
.page-nav .drop-down li.last,
.site-nav .drop-down li.last {
	border:0;	
}
.page-nav .drop-down a:visited,
.site-nav .drop-down a:visited,
.page-nav .drop-down a,
.site-nav .drop-down a {
	display:block;
	white-space:nowrap;
	color:#333;
	font-weight:100;
	padding:3px 10px;
	-moz-border-radius:0;
	min-width:150px;
	font-size:11px !important;
}
.page-nav .drop-down a:hover ,
.site-nav .drop-down a:hover {
	background-color:#cddce3;
	background-image:none;
}
/*PAGE STATS*/
.page-stats {
	padding:5px;	
}
.page-stats span {
	display:block;	
	padding:0 0 5px 0;
	color:#666;
}
/*RELATED PAGES*/
.related-tag {
	margin:0 0 10px 0;	
}
/*DMENU*/
.deki-file-menu li a {
	padding:5px;
	display:block;
}
.deki-file-menu li a:hover {
	text-decoration:none;
	background:#efefef;	
}
.deki-file-menu li a .icon {
	margin-right:5px;	
	vertical-align:middle;
}
/*Pagination*/
.pagination {
	text-align: center;	
	margin: 4px 0;
}
.pagination span.prev {
	margin-right: 16px;
	padding-left: 14px;
}
.pagination span.next {
	margin-left: 16px;
	padding-right: 14px;
}
.pagination {
	font-size: 11px;
	color: #888;
}
.pagination span.prev {
	background: url(images//skins/common/icons/arrow-l.gif) no-repeat center left; 
}
.pagination span.next {
	background: url(images//skins/common/icons/arrow-r.gif) no-repeat center right; 
}
.pagination span.info {
	font-weight: bold;
	color: #333;
	font-size: 12px;
}

/*COMMENTS*/
.commentMore {
	margin:0 0 10px 0;	
}
.commentNum {
	float:left;	
}
.comment {
	margin:5px 0;
	padding:5px;
	border-bottom:1px solid #efefef;
}
.comments .commentText {
	margin:0 0 0 30px;
}
.commentActions {
	float:right;	
}
textarea.commentText {
	width:70%;
	height:80px;
	padding:5px;	
}
/*IE6*/
* html body {
	text-align:center;	
}
* html body .site-head {
	background-image:url(images/site_head_bg.gif);	
}
* html body .site-mast {
	background-image:url(images/site_mast_bg.gif);
	background-color:#5c9cca;	
}
* html body .site-head,
* html body .global {
	text-align:left;
}
* html body .site-logo {
	padding:3px 3px 0 3px;	
}
* html body .comment {
	padding-top:0 ;
}
* html body .user-nav ul,
* html body .page-nav ul {
	height:100%;	
	overflow:visible;
}
* html body td, th {
	font-size:12px;
}
* html body .dmenu-body {
	text-align:left;	
}
/*SiteNav and PageNav*/
* html body .flex-logo {
	background-image:url(images/flex_waves.gif);
	background-position:top center;
}
* html body .page-nav ul {
	margin-right:35%;
}
* html body .right-bar {
	width:33%;
}
* html body .site-nav li span, 
* html body .site-nav li a {
	display:inline !important;
	width:auto;
}
* html body .site-nav li,
* html body .page-nav li {
	display:inline;
	width:auto;
}
* html body .page-nav .drop-down a,
* html body .site-nav .drop-down a {
	width:100%;
}
* html body .site-nav li.site-search .textinput{
	width:100px;
}
* html body #deki-page-alerts .legend {
	width:250px;
}



/* --------- _CONTENT.CSS --------- */
body {
	font-family: arial,verdana,helvetica ;
	font-size: 12px;
	line-height: 1.5;
}
blockquote {
	margin: 0 3em;	
}
a {
	color: #36c;
	text-decoration:none;
}
a.disabled:hover,
a.disabled {
	background-color:transparent!important;
	text-decoration:none !important;
	cursor:pointer;
	opacity:.5 !important;
	color:#999 !important;
}
em {
	font-style: italic;	
}
strong {
	font-weight:bold;	
}
strong em,
em strong {
	font-weight:bold;	
	font-style:italic;
}
a.new {
	text-decoration: none;
	border-bottom: 1px dotted #af6666;
	color: #af6666;	
}
a.new:hover {
	color: #790000;
	border-bottom: 1px solid #790000;
}
a:hover {
	color: #004a80;
	text-decoration:underline;
}
a.disabled:hover,
a.disabled {
	cursor:default;
	text-decoration:none;
}
p, 
blockquote, 
pre,
h2, 
h3, 
h4, 
h5, 
h6, 
ol, 
ul, 
dl {
	margin: 0.5em 0 ;
}

ol, 
ul, 
dd {
	padding-left: 2em; 
}
ol li {
	list-style-type: decimal;
}
div.wiki-toc ol li {
	list-style-type: none;
}
ul li {
	list-style-type: disc;
}
ul ul, 
ul ol, 
ol ul, 
ol ol {
	margin-top: 0;
	margin-bottom: 0;
}
ol ul, 
ul ul	{
   list-style-type: circle;
}

ol ol ul, 
ol ul ul, 
ul ol ul, 
ul ul ul {
	list-style-type: square;
}
blockquote {
	border-top: 1px dotted #aaa;
	border-bottom: 1px dotted #aaa;
	margin-left: 1.8em;
	margin-right: 1.8em;
	padding: 0.6em;
	text-align: center;
	color: #777;
	font-size: 12px;
}
/*** 
 * specificity kills us here
 */
body.deki-content-edit span.comment,
body.deki-content-edit div.comment, 
body.deki-content-edit p.comment {
	background-color: #fff799;
	padding: 3px;
}
code {
	font-family: "Lucida Console", Courier, Monospace;
	font-size: 14px;
	color: #003471;
}
pre {
	color: #777;
	margin-left: 1em;
	padding-left: 1em;
	border-left: 4px solid #aaa;
	background-color: #fefefe;
	overflow: visible;
}
/** 
	Editor scripting styles 
*/
body.deki-content-edit pre.script {
	color: #004184;
	font-size: 12px;
	line-height: 18px;
}
h2, 
h3, 
h4, 
h5, 
h6 {
	padding: 0;
	padding-top: 0.375em;
	margin-bottom: 10px;
	line-height: 1;
}

#deki-new-page-title,
h1,
.header_1,
#body div.title h1 {
	color: #333;
	font-size: 28px;
	line-height: 1.2;
	margin:0;
	padding:0 0 5px 0;
}
h1#title {
	border-bottom:1px dotted #aaa;
}
#deki-new-page-title {
	margin:10px 0;
	width:450px;	
}
h2,
.header_2 {
	font-size: 26px;
	color:#365f91;
}
h3,
.header_3 {
	font-size: 24px;
	color:#4f81bd;
}
h4,
.header_4 {
	font-size: 22px;
	color: #4f81bd;
}
h5,
.header_5 {
	font-size: 20px;
	color: #333;
}
h6,
.header_6 {
	font-size: 18px;
	color: #666;
}

/**
	Table Styles
*/
table {
	border: 1px solid #aaa;
}
table th {
	color: #4f6b72;
	border-bottom: 1px solid #aaa;
	border-right: 1px solid #aaa;
	background: url(images/bg-tbl-header.gif) no-repeat;
	background-color: #d9d9d9;
	font-size:13px;
	padding:2px 5px;
	font-weight:bold;
}
table td {
	color: #4f6b72;
	padding:5px;
}
table td.bg2, 
table tr.bg2 td {
	background-color: #f5f8fe;	
}

/* script styles */
pre.script {
	padding-left: 12px;
	padding-top: 16px;
	background: transparent url(/skins/common/images/bg-script.png) no-repeat top left;
	border: 1px solid #c66;
	border-width: 1px 1px 1px 5px;
	color: #004184;
}
pre.script-jem {
	padding-left: 12px;
	padding-top: 16px;
	background: transparent url(/skins/common/images/bg-script-jem.png) no-repeat top left;
	border: 1px solid #c96;
	border-width: 1px 1px 1px 5px;
	color: #004184;
}
pre.script-css {
	padding-left: 12px;
	padding-top: 16px;
	background: transparent url(/skins/common/images/bg-script-css.png) no-repeat top left;
	border: 1px solid #66c;
	border-width: 1px 1px 1px 5px;
	color: #004184;
}

