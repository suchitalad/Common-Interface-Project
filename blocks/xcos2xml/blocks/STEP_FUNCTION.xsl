    <xsl:template match="*[@interfaceFunctionName = 'STEP_FUNCTION']">
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
        <Object display_parameter="" as="displayProperties"/>
        <Object p000_value="1" p001_value="0" p002_value="1" as="parameter_values"/>
      </xsl:element>
    </xsl:template>