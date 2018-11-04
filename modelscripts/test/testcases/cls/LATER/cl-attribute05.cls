    // tags, id, readOnly

        //@Metric "plain class" 1
        //@Metric "class" 1
        //@Metric "association class" 0

class model Cl_class02

class A
    attributes
        g : Integer {tag1, tag2}
        h : Integer{tag1, id}
        i : Integer{tag1, readOnly}
        j : Integer{tag1, id, readOnly}