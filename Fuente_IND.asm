      *DIRECCIONAMIENTO INDEXADO

      ORG $8000

      LDAA   $45,X          *INDEXADO X: CARGA (X+$45) EN A
      LdAB   $67,Y          *INDEXADO Y: CARGA (Y+$67) EN B
      LDD    $17,X          *INDEXADO X: CARGA (X+$17) EN D
      ldx    $F1,Y          *INDEXADO Y: CARGA (Y+$F1) EN X
      ADDA   $07,Y          *INDEXADO Y: SUMA (Y+$07) A A
      Anda   $F0,X          *INDEXADO X: AND (X+$F0) CON A
      ldY    $A0,Y          *INDEXADO Y: CARGA (Y+$A0) EN Y

      END
