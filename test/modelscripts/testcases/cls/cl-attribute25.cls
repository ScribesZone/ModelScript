    //@Metric "class" 1
    //@Metric "plain class" 1
    //@Metric "association" 0
    //@Metric "plain association" 0
    //@Metric "association class" 0
    //@Metric "attribute" 3

class model Cl_class03

class A
    attributes
        /  a : Integer[0..1] {id}
        / - b : Integer[0..1] {id}
        % c : Integer[0..1] {id,readOnly}
