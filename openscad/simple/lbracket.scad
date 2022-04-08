include <roundedcube.scad>;

// one side
difference() {
    roundedcube([20,5,20], false, 2, "y");
    
    translate([10, 10, 10]) {
        rotate([90, 0, 0]) {    
        cylinder(20, 3, 3);
        }
    }
}

// other side

rotate([0,0,90]) {
    difference() {
        roundedcube([25,5,20], false, 2, "y");
    
        translate([15, 10, 10]) {
            rotate([90, 0, 0]) {    
            cylinder(20, 3, 3);
            }
        }
    }
}

// Square off the corner
cube([5,5,20]);
rotate([0,0,90])
    cube([5,5,20]);




