use <card_holder.scad>
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
module stackable_box(length=60,width=40,height=30,thickness=2,tolerance=0.5,bottom=false, max_angle=30) {
    difference() {
        union() {
            cube([width,length,thickness]);
            if (!bottom) { base(length=length,width=width,thickness=thickness,max_angle=max_angle); }
            cube([width,thickness,height]);
            cube([thickness,length,height]);
            translate([0,length-thickness,0]) cube([width,thickness,height]);
            translate([width-thickness,0,0]) cube([thickness,length,height]);
        };
        translate([0,0,height]) base(length=length,width=width,thickness=thickness,max_angle=max_angle);
    };
};



// Critter pieces box (x10)
//stackable_box(width=58, length=67.5, height=15);

// Special event card & forest card boxes (x2)
//card_holder(card_width=46, card_height=65, height=28, stackable=true);

// Card holders for expansion cards (x1)
//card_holder(card_width=46, card_height=65, height=15, stackable=true); 
card_holder(card_width=46, card_height=65, height=11, stackable=true);

//base(thickness=2);
