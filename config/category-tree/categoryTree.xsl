<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h2>Category Tree</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Category ID</th>
        <th>Category Name</th>
        <th>Parent</th>
      </tr>
      <xsl:for-each select="GetCategoriesResponse/CategoryArray/Category">
        <tr>
          <td><xsl:value-of select="CategoryID"/></td>
          <td><xsl:value-of select="CategoryName"/></td>
          <td><xsl:value-of select="CategoryParentID"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>