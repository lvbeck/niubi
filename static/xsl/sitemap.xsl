<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xna="http://www.sitemaps.org/schemas/sitemap/0.9" exclude-result-prefixes="xna">
<xsl:output indent="yes" method="html" omit-xml-declaration="yes"/>
<xsl:template match="/">
<html>
<body>
<h2>Site Map</h2>
<table border="0" width="100%">
<xsl:for-each select="xna:urlset/xna:url">
<tr>
<td>Update Freq: <xsl:value-of select="xna:changefreq"/></td>
<td>URL: <xsl:value-of select="xna:loc"/></td>
<td>Priority: <xsl:value-of select="xna:priority"/></td>
</tr>
</xsl:for-each>
</table>
</body>
</html>
</xsl:template>
</xsl:stylesheet> 