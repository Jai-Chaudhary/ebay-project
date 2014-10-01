<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h2>ITEM SPECIFICS</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Item ID</th>
        <th>Title</th>
        <th>Country</th>
        <th>Primary Category</th>
        <th>Specifics</th>
        <th>Condition></th>
        <th>Image</th>
      </tr>
      <xsl:for-each select="GetMultipleItemsResponse/Item">
        <tr>
          <td><xsl:value-of select="ItemID"/></td>
          <td><xsl:value-of select="Title"/></td>
          <td><xsl:value-of select="Country"/></td>
          <td><xsl:value-of select="PrimaryCategoryName"/></td>
          <td>
            <ul>
              <xsl:for-each select="ItemSpecifics/NameValueList">
                <li>
                  <span>
                    <xsl:value-of select="Name"/> : 
                    <xsl:value-of select="Value"/>
                  </span>
                </li>
              </xsl:for-each>
            </ul>
          </td>
          <td><xsl:value-of select="ConditionDisplayName"/></td>
          <td>
            <img>
              <xsl:attribute name="src">
                  <xsl:value-of select="GalleryURL"/>
              </xsl:attribute>
            </img>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>