include <roundedcube.scad>;

desk_thickness = 17;

// vertical piece
translate([-2.5,0,0])
cube([60,5,20]);

// Top part
rotate([0,0,90])
  roundedcube([50,5,20], false, 2, "z");

// Clip...
translate([desk_thickness + 7,0,0])
rotate([0,0,90])
  cube([20,5,20]);
// ...with Tensioners
translate([desk_thickness + 2,16.5,0])
  cylinder(h=20, r=3.5);

// Bottom Part
translate([60,0,0])
rotate([0,0,90])
  roundedcube([60,5,20], false, 2, "z");
  
// Hooky bit
translate([30,55,0])
  roundedcube([30, 5, 20], false, 2, "z");

