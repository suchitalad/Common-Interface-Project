    <xsl:template match="*[@interfaceFunctionName = 'M_freq']">
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
        <xsl:attribute name="explicitInputPorts">0</xsl:attribute>
        <xsl:attribute name="implicitInputPorts">0</xsl:attribute>
        <xsl:attribute name="explicitOutputPorts">0</xsl:attribute>
        <xsl:attribute name="implicitOutputPorts">0</xsl:attribute>
        <xsl:attribute name="controlPorts">1</xsl:attribute>
        <xsl:attribute name="commandPorts">
          <xsl:variable name="value" select="(*[@as='exprs']/data[1]/@value)" />
          <xsl:variable name="count" select="string-length($value) - string-length(translate($value, ';, ', '')) + 1" />
          <xsl:variable name="power">
            <xsl:call-template name="pow">
              <xsl:with-param name="pBase" select="2"/>
              <xsl:with-param name="pPower" select="$count"/>
            </xsl:call-template>
          </xsl:variable>
          <xsl:variable name="integer-power" select="floor($power)"/>
          <xsl:value-of select="$integer-power - 1"/>
        </xsl:attribute>
        <xsl:attribute name="simulationFunction">
          <xsl:value-of select="@simulationFunctionName" />
        </xsl:attribute>
        <xsl:attribute name="sourceVertex">0</xsl:attribute>
        <xsl:attribute name="targetVertex">0</xsl:attribute>
        <xsl:attribute name="tarx">0</xsl:attribute>
        <xsl:attribute name="tary">0</xsl:attribute>
        <xsl:apply-templates select="node()"/>
        <Object>
          <xsl:attribute name="display_parameter">
            <xsl:value-of select="@value"/>
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
