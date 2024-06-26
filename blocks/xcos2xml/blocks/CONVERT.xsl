    <xsl:template match="*[@interfaceFunctionName = 'CONVERT']">
      <xsl:element name="mxCell">
        <xsl:attribute name="style">
          <xsl:value-of select="@style" />
        </xsl:attribute>
        <xsl:attribute name="id">
          <xsl:value-of select="@id" />
        </xsl:attribute>
        <xsl:attribute name="vertex">1</xsl:attribute>
        <xsl:attribute name="connectable">0</xsl:attribute>
        <xsl:attribute name="CellType">Component</xsl:attribute>
        <xsl:attribute name="blockprefix">XCOS</xsl:attribute>
        <xsl:attribute name="explicitInputPorts">1</xsl:attribute>
        <xsl:attribute name="implicitInputPorts">0</xsl:attribute>
        <xsl:attribute name="explicitOutputPorts">1</xsl:attribute>
        <xsl:attribute name="implicitOutputPorts">0</xsl:attribute>
        <xsl:attribute name="controlPorts">0</xsl:attribute>
        <xsl:attribute name="commandPorts">0</xsl:attribute>
        <xsl:attribute name="simulationFunction">
          <xsl:value-of select="@simulationFunctionName" />
        </xsl:attribute>
        <xsl:attribute name="sourceVertex">0</xsl:attribute>
        <xsl:attribute name="targetVertex">0</xsl:attribute>
        <xsl:attribute name="tarx">0</xsl:attribute>
        <xsl:attribute name="tary">0</xsl:attribute>
        <xsl:apply-templates select="node()"/>
        <Object>
          <xsl:variable name="exprsData" select="(*[@as='exprs']/data[1]/@value)" />
          <xsl:variable name="dataValue" select="*[@as='exprs']/data[2]/@value" />
          <xsl:variable name="displayParam1">
            <xsl:choose>
              <xsl:when test="$exprsData = 1 or $exprsData = 2">
                <xsl:text>decim</xsl:text>
              </xsl:when>
              <xsl:when test="$exprsData = 3">
                <xsl:text>int32</xsl:text>
              </xsl:when>
              <xsl:when test="$exprsData = 4">
                <xsl:text>int16</xsl:text>
              </xsl:when>
              <xsl:when test="$exprsData = 5">
                <xsl:text>int8</xsl:text>
              </xsl:when>
              <xsl:when test="$exprsData = 6">
                <xsl:text>uint32</xsl:text>
              </xsl:when>
              <xsl:when test="$exprsData = 7">
                <xsl:text>uint16</xsl:text>
              </xsl:when>
              <xsl:when test="$exprsData = 8">
                <xsl:text>uint8</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:text></xsl:text>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>
          <xsl:variable name="displayParam2">
            <xsl:choose>
              <xsl:when test="$dataValue = 1 or $dataValue = 2">
                <xsl:text>decim</xsl:text>
              </xsl:when>
              <xsl:when test="$dataValue = 3">
                <xsl:text>int32</xsl:text>
              </xsl:when>
              <xsl:when test="$dataValue = 4">
                <xsl:text>int16</xsl:text>
              </xsl:when>
              <xsl:when test="$dataValue = 5">
                <xsl:text>int8</xsl:text>
              </xsl:when>
              <xsl:when test="$dataValue = 6">
                <xsl:text>uint32</xsl:text>
              </xsl:when>
              <xsl:when test="$dataValue = 7">
                <xsl:text>uint16</xsl:text>
              </xsl:when>
              <xsl:when test="$dataValue = 8">
                <xsl:text>uint8</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:text></xsl:text>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>
          <xsl:attribute name="display_parameter">
            <xsl:value-of select="concat($displayParam1, ',', $displayParam2)" />
          </xsl:attribute>
          <xsl:attribute name="as">displayProperties</xsl:attribute>
        </Object>
        <Object>
          <xsl:for-each select="*[@as='exprs']/data">
            <xsl:attribute name="{concat('p', format-number(position() - 1, '000'), '_value')}">
              <xsl:value-of select="@value"/>
            </xsl:attribute>
          </xsl:for-each>
          <xsl:attribute name="as">parameter_values</xsl:attribute>
        </Object>
      </xsl:element>
    </xsl:template>
