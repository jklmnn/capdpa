with System;

package Capdpa.Outer
is
   package Inner
   is
      type Class is
      limited record
         null;
      end record
      with Import, Convention => CPP;
      type Class_Address is access Class;
      function Constructor return Class;
      pragma Cpp_Constructor (Constructor, "_ZN5Outer5InnerC1Ev");
   end Inner;
   type Class is
   limited record
      I : Capdpa.Outer.Inner.Class;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN5OuterC1Ev");
end Capdpa.Outer;
