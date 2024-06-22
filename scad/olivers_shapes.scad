module rounded_square(length=20, width=20,d=5) {
    union () {
        translate([0,d/2,0]) square([width,length-d]);
        translate([d/2,0,0]) square([width-d,length]);
        translate([d/2,d/2,0]) circle(d=d);
        translate([width-d/2,d/2,0]) circle(d=d);
        translate([width-d/2,length-d/2,0]) circle(d=d);
        translate([d/2,length-d/2,0]) circle(d=d);
    };
};