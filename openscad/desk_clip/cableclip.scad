// A simple cable clip for your desk.

// See https://danielupshaw.com/openscad-rounded-corners/
// Or https://gist.github.com/groovenectar/92174cb1c98c1089347e
include <roundedcube.scad>;


// This is about the thickness of an IKEA BEKANT standing desk, FYI.
desk_thickness = 17;

// Modify below at own risk (of being confused by openscad, like me).

// vertical piece
translate([-2.5,0,0])
cube([60,5,20]);

// Top part
rotate([0,0,90])
  roundedcube([50,5,20], false, 2, "z");

// Clip...
translate([desk_thickness + 6.5,0,0])
rotate([0,0,90])
  cube([40,5,20]);
// ...with Tensioners
translate([desk_thickness + 1.5,36.5,0])
  cylinder(h=20, r=3.5);
translate([desk_thickness + 1.5,15,0])
  cylinder(h=20, r=3.5);

// Bottom Part
translate([60,0,0])
rotate([0,0,90])
  roundedcube([60,5,20], false, 2, "z");
  
// Hooky bit
translate([30,55,0])
  roundedcube([30, 5, 20], false, 2, "z");

