// Overall dimensions
total_len = 200;
total_height = 25;
total_width = 50;

// Side rail dimensions.
rail_thickness = 5;
// The angle the rail end turns before going 90deg
railend_angle = 25;
// The overall length between the angled turn and the end of the model.
railend_len = 35;

// Rung dimensions. Rungs are alaways centred, and there is always one at the corners of the siderails.
rung_thickness = 3;
// nuber of rungs in the main ladder length, not including
// corner rungs.
rung_maincount = 6;
// number of rungs in the end section (each). This doesn't
// include the corner rungs.
rung_endcount = 2;

// Here be dwagons.

module railend()
{
    
    // the side opposite railend_angle
    railend_zoffset = tan(railend_angle) * railend_len;
    railend_hyplen = sqrt(railend_zoffset^2 + railend_len^2);
    
    // The end of the wee legs
    translate ([0,0,railend_zoffset])
        cube([rail_thickness, rail_thickness, (total_height - railend_zoffset)]);
    
    // The angled bit.    
    translate([0, railend_len, 0])
    rotate(a=[90-railend_angle,0,0]) 
        cube([rail_thickness, rail_thickness, railend_hyplen]);
}

module siderail()
{
    railend();

    translate([0,railend_len,0]) 
    cube([rail_thickness,(total_len - (2*railend_len)),rail_thickness]);

    translate([rail_thickness,total_len,0])
        rotate([0,0,180])
        railend();
}

module rungs(count, ystart, yend, zstart, zend)
{
    for (i = [1 : count])
    {
        echo(i);
        start = railend_len;
        end = total_len-railend_len-rail_thickness;
        rung_yoffset = (yend - ystart) / (count+1);
        rung_zoffset = (zend - zstart) / (count+1);
        echo (ystart+(i*rung_yoffset));
        translate([0,ystart+(i*rung_yoffset), zstart+(i*rung_zoffset) + rungdiff])
            cube([total_width, rung_thickness, rung_thickness]);
    }
}
// The two side rails
siderail();
translate([50-rail_thickness, 0, 0]) siderail();

// The "mandatory" rungs at turning points in the side rails

rungdiff = (rail_thickness-rung_thickness)/2;

translate([0, railend_len, rungdiff])
    cube([total_width, rung_thickness, rung_thickness]);

translate([0, total_len-railend_len-rung_thickness, rungdiff])
    cube([total_width, rung_thickness, rung_thickness]);

translate([0,rungdiff,tan(railend_angle) * railend_len])
    cube([total_width, rung_thickness, rung_thickness]);
    
translate([0,total_len-rung_thickness-rungdiff,tan(railend_angle) * railend_len])
    cube([total_width, rung_thickness, rung_thickness]);  

// Main length rungs
rungs(rung_maincount, railend_len, total_len-railend_len, 0,0);

// End rail rungs
rungs(rung_endcount, 0, railend_len, tan(railend_angle) * railend_len, 0);
rungs(rung_endcount, total_len-railend_len, total_len-(rail_thickness/2), 0, tan(railend_angle) * railend_len);