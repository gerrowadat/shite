// Hopefully obvious parameters. Sizes in mm
radius = 30;
height = 20;
thickness = 1;
// Total number of segments
segments = 15;

segment_angle = 360 / segments;


// The bottom of the box
cylinder(h=thickness, r=radius);

// Centre Cylinder
cylinder(h=height+2, r=radius/4);

// The wall of the box
difference() { 
    cylinder(h=height, r=radius);
    cylinder(h=height+1, r=radius-thickness);
}

// The first segment divider


for (i = [0 : segments] ) {
    this_angle = segment_angle * i;
    rotate(this_angle) {
        translate([0, (thickness / 2) * -1, 0]) {
            cube([radius+1, thickness, height]);
        }
    }
}


// Lid part
translate([radius*2+10, 0, 0]) {
  
   difference () {
       // Base
       cylinder(h=thickness, r=radius+1);
           
       translate([0,0,-1]) {
       difference() {
           intersection() {
               cylinder(h=thickness+3, r=radius+1);
               linear_extrude(height=thickness+4) {
                   // Triangles are easier than circles no you shut up.
                   polygon([[0,0],[0,radius*2], [(radius*2)*tan(segment_angle), radius*2]]);
               }            };
           cylinder(h=thickness+5, r=radius/4);
       };
   }

    }

    // Outer rim
    difference() { 
        cylinder(h=height/3, r=radius+1);
        cylinder(h=height/3+1, r=radius+1-thickness);
    }
    // lid 'bearing'
    difference () {
        cylinder(h=thickness+2, r=(radius/4)+thickness);
        cylinder(h=thickness+3, r=(radius/4)+0.1);
    }
}

    