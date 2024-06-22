use <stackable_box.scad>
$fa = 1;
$fs = 0.4;
module slot(width,depth,height,thickness,rounded_slot=true) {
    difference() {
        union () {
            translate([-width/2,-0.001,thickness]) cube([width,thickness+0.002,height]);
            translate([0,depth-width/2,-thickness-0.001]) cylinder(d=width,h=2*thickness+0.003);
            translate([-width/2,-0.001,-thickness-0.001]) cube([width,depth-width/2,2*thickness+0.003]);
            //Cutout in preparation for rounded edges
            if (rounded_slot) {translate([-width,-0.001,height-width/2+0.001]) cube([width*2,thickness+0.002,width/2+0.002]);}
        };
        //Rounded edges of slot
        if (rounded_slot) {
            translate([-width,thickness+0.003,height-width/2]) rotate([90,0,0]) cylinder(d=width,h=thickness+0.004);
            translate([width,thickness+0.003,height-width/2]) rotate([90,0,0]) cylinder(d=width,h=thickness+0.004);
        }
    };
};
module card_holder(card_width=64,card_height=89,thickness=2,height=40,slot_width=20,slot_depth=20,tolerance=0.5,slots=[1,0,0,0],rounded_slot=true,stackable=false,max_angle=30) {
    card_height=card_height+2*tolerance;
    card_width=card_width+2*tolerance;
    base_height=2*thickness+card_height;
    base_width=2*thickness+card_width;
    full_height = stackable ? height - thickness : height;
    union() {
        difference() {
            union() {
                //base
                
                if (stackable) { base(length=base_width,width=base_height,thickness=thickness,max_angle=max_angle); }
                else {cube([base_height,base_width,thickness]);}
                //width walls
                cube([thickness,base_width,full_height]);
                translate([base_height-thickness,0,0]) cube([thickness,base_width,full_height]);
                //height walls
                cube([base_height,thickness,full_height]);
                translate([0,base_width-thickness,0]) cube([base_height,thickness,full_height]);
            };
            if(slots[0] == 1) {
                translate([base_height/2,0,0]) slot(width=slot_width,depth=slot_depth,height=full_height,thickness=thickness,rounded_slot=rounded_slot);
            };
            if(slots[1] == 1) {
                translate([0,base_width/2,0]) rotate([0,0,270]) slot(width=slot_width,depth=slot_depth,height=full_height,thickness=thickness,rounded_slot=rounded_slot);
            };
            if(slots[2] == 1) {
                translate([base_height/2,base_width,0]) rotate([0,0,180]) slot(width=slot_width,depth=slot_depth,height=full_height,thickness=thickness,rounded_slot=rounded_slot);
            };
            if(slots[3] == 1) {
                translate([base_height,base_width/2,0]) rotate([0,0,90]) slot(width=slot_width,depth=slot_depth,height=full_height,thickness=thickness,rounded_slot=rounded_slot);
            }
            if(stackable) {translate([0,0,full_height]) base(length=base_width,width=base_height,thickness=thickness,max_angle=max_angle);}
        };
    };
};
card_holder(height=20,stackable=true);
//slot(width=20,deph=20,thickness=2,height=30);