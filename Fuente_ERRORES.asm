*ARCHIVO DE PRUEBA DE ERRORES - MC68HC11
*Basado en el SET DE INSTRUCCIONES UNAM
*Cada bloque provoca un error especifico del compilador

      ORG $8000

*---------------------------------------------
* ERROR 009: mnemónico sin espacio al margen
*---------------------------------------------
nop                    *9 INSTRUCCION CARECE DE ESPACIO RELATIVO AL MARGEN

*---------------------------------------------
* ERROR 011: etiqueta con comentario en la misma línea
*---------------------------------------------
ETIQ1      *ETIQUETA DUPLICADA

*---------------------------------------------
* ERROR 013: etiqueta duplicada (ETIQ1 ya existe)
*---------------------------------------------
INICIO
      LDX #1789
CICLO
      NOP
      nop
      NOP
      NoP
      NOP

*---------------------------------------------
* ERROR 001: constante inexistente (#CONSTANTE1 no definida)
*---------------------------------------------
      AdcA #CONSTANTE1   * 1 CONSTANTE INEXISTENTE

*---------------------------------------------
* ERROR 004: mnemónico inexistente (NP no existe)
*---------------------------------------------
      NP                 * 4 MNEMONICO INEXISTENTE

*---------------------------------------------
* ERROR 002: variable inexistente (VARIABLE1 no definida en EQU)
*---------------------------------------------
      AdcA VARIABLE1     * 2 VARIABLE INEXISTENTE

*---------------------------------------------
* ERROR 004: mnemónico inexistente en EXT (LX no existe)
*---------------------------------------------
      LX $FF             *4 MNEMONICO INEXISTENTE

*---------------------------------------------
* ERROR 005: instrucción sin operando (ANDA necesita operando)
*---------------------------------------------
      ANDA               * 5 INSTRUCCION SIN OPERANDO

*---------------------------------------------
* ERROR 006: instrucción INH con operando (DEX no lleva operando)
*---------------------------------------------
      dex #$45           *6 INSTRUCCION NO LLEVA OPERANDOS

*---------------------------------------------
* ERROR 003: etiqueta inexistente en salto relativo
*---------------------------------------------
      BNE CICLO2         * 3 ETIQUETA INEXISTENTE

*---------------------------------------------
* ERROR 008: salto relativo muy lejano
*---------------------------------------------
      BnE CICLO          * 8 SALTO RELATIVO MUY LEJANO (CICLO está muy lejos)

*---------------------------------------------
* ERROR 007: magnitud de operando errónea (>65535 en INM)
*---------------------------------------------
      LDX #$12345        * 7 MAGNITUD ERRONEA

*---------------------------------------------
* ERROR 007: magnitud > 65535 en binario
*---------------------------------------------
      LDX #%11111111111111111  * 7 MAGNITUD ERRONEA

*---------------------------------------------
* ERROR 007: magnitud > 65535 en octal
*---------------------------------------------
      LDX #&7777777777   * 7 MAGNITUD ERRONEA

*---------------------------------------------
* ERROR 007: magnitud > 65535 en decimal
*---------------------------------------------
      LDX #123456789     * 7 MAGNITUD ERRONEA

*---------------------------------------------
* ERROR 007: carácter ASCII con más de 1 caracter
*---------------------------------------------
      LDX #'adcdef       * 7 MAGNITUD ERRONEA (ASCII >1 caracter)

*---------------------------------------------
* Instrucciones correctas mezcladas como referencia
*---------------------------------------------
      LDAA #$00          *CORRECTO INM
      STAA $1000         *CORRECTO DIR
      LDAB $FF           *CORRECTO DIR
      LDD #$302C         *CORRECTO INM
      JMP INICIO         *CORRECTO JMP

*---------------------------------------------
* ERROR 007: magnitud errónea en INDX
*---------------------------------------------
      LDX $12,X          *CORRECTO
      LDX $777,X         * 7 MAGNITUD ERRONEA (>255 en indexado)

*---------------------------------------------
* ERROR 007: magnitud errónea en INDY
*---------------------------------------------
      LDX $12345,y       * 7 MAGNITUD ERRONEA (>255 en indexado)
      LDX #%11111111111111111,Y * 7 MAGNITUD ERRONEA

*---------------------------------------------
* ERROR 007: magnitud > 65535 en INDX decimal
*---------------------------------------------
      LDX 123456789,Y    * 7 MAGNITUD ERRONEA

*---------------------------------------------
* ERROR 007: ASCII de mas de 1 caracter en INDY
*---------------------------------------------
      LDX 'adcdef,Y      * 7 MAGNITUD ERRONEA

*---------------------------------------------
* Más instrucciones sin error como referencia
*---------------------------------------------
ETIQ1                    *ERROR 012: ETIQUETA DUPLICADA

      LDX $FFFE          *CORRECTO EXT (cerca del límite)
      ldx VARIABLE       *correcto si VARIABLE fuera EQU

*---------------------------------------------
* ERROR 010: programa sin END (comentar la siguiente linea para provocarlo)
*---------------------------------------------
      END
