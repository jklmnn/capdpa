with System;
with Tests;
with Interfaces.C;
with Test_Private_Void_Pointer_Member.Cls;

procedure Main
is
   use type System.Address;
   use Test_Private_Void_Pointer_Member;
   Inst : aliased Cls.Class := Cls.Constructor (System'To_Address (1234567));
begin
   Tests.Assert (Cls.Get (Inst'Access) = System'To_Address (1234567), "Wrong value returned (1): ");
end Main;
