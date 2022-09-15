// Hopefully obvious parameters. Sizes in mm
radius = 30;
height = 20;
thickness = 2;
// Total number of segments
segments = 7;

segment_angle = 360 / segments;


// The bottom of the box
cylinder(h=thickness, r=radius);

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
            cube([radius, thickness, height]);
        }
    }
}

