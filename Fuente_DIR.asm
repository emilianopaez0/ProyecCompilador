      *DIRECCIONAMIENTO DIRECTO

      ORG $8000

      LDAA   $45            *DIRECTO: CARGA DIR $45 EN A
      Ldab   11             *DIRECTO: CARGA DIR 11 EN B
      ldd    $17            *DIRECTO: CARGA DIR $17 EN D
      LDX    15             *DIRECTO: CARGA DIR 15 EN X
      AdDA   $7C            *DIRECTO: SUMA DIR $7C A A
      andA   $F0            *DIRECTO: AND DIR $F0 CON A
      LDY    $AB            *DIRECTO: CARGA DIR $AB EN Y

      END
