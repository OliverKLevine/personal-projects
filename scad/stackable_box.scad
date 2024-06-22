use <card_holder.scad>
use <olivers_shapes.scad>
$fa = 1;
$fs = 0.4;
module base(length=60,width=40,thickness=2,max_angle=30) {
    w = thickness*tan(max_angle);
    polyhedron(
        points=[ 
            [0,0,0],
            [width,0,0],
            [width,length,0],
            [0,length,0],
            [w,w,-thickness],
            [width-w,w,-thickness],
            [width-w,length-w,-thickness],
            [w,length-w,-thickness]
        ],
        faces = [
            [0,3,2,1],
            [0,1,5,4],
            [1,2,6,5],
            [2,3,7,6],
            [3,0,4,7],
            [4,5,6,7]
        ]
    );
};
module stackable_box_lid(length=60,width=40,thickness=2,tolerance=0.5, max_angle=30) {
    d=0.001;
    //base
    translate([0,0,0]) union () {
        cube([width,length,thickness]);
        base(length,width,thickness,max_angle);
    };
};
module stackable_box(length=60,width=40,height=30,thickness=2,tolerance=0.5,bottom=false,top=false, max_angle=30) {
    full_height = bottom ? height : height - thickness;
    difference() {
        union() {
            if (!bottom) { base(length=length,width=width,thickness=thickness,max_angle=max_angle); }
            else {cube([width,length,thickness]);}
            cube([width,thickness,full_height]);
            cube([thickness,length,full_height]);
            translate([0,length-thickness,0]) cube([width,thickness,full_height]);
            translate([width-thickness,0,0]) cube([thickness,length,full_height]);
        };
        if(!top) {translate([0,0,full_height]) base(length=length,width=width,thickness=thickness,max_angle=max_angle);};
    };
};
module stackable_circle_holder(width=40,length=60,height=30,d=30,thickness=2,top=false) {
    union () {
        stackable_box(width=width, length=length, height=height,top=top);
        difference() {
            union() {
                cube([width,length,d/2]);
                triangle_height=height-d/2-2*thickness;
                triangle_width=(length-d-2*thickness)/2;
                translate([0,thickness,d/2]) linear_extrude(height=triangle_height,scale=[1,0])  square(size=[width,triangle_width]);
                rotate([0,0,180]) translate([-width,-length+thickness,d/2]) linear_extrude(height=triangle_height,scale=[1,0])  square(size=[width,triangle_width]);
            };
            translate([thickness + 0.001,length/2,d/2]) rotate([0,90,0]) cylinder(h=width-2*thickness-0.002,d=d);
        };
    };
};



