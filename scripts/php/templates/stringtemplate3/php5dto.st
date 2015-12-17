<?

class $class.name$
{
	$class.variables.values:{ var | public var \$$var.name$ = $var.init$;};separator="\n"$
        $class.objects.values:{ var | public var \$$var.name$ = $var.init$;};separator="\n"$
        $class.collections.values:{ var | public var \$$var.name$ = $var.init$;};separator="\n"$
        $class.properties.values:{ var | private var \$$var.name$ = $var.init$;};separator="\n"$
        
	public function $class.name$()
	{
	}
        
        $class.properties.values:{ var | 
        $if(var.writable)$public function set$var.capitalize$(\$value){\$this->$var.name$ = \$value;}$endif$
        $if(var.readable)$public function get$var.capitalize$(){return \$this->$var.name$;}$endif$};separator="\n"$
        
        public function clone()
        {
        	var \$clone = new $class.name$();
                $class.variables.values:{ var | \$clone->$var.name$ = \$this->$var.name$;};separator="\n"$
                $class.properties.values:{ var | $if(var.writable)$\$clone->set$var.capitalize$($if(var.readable)$\$this->get$var.capitalize$()$else$\$this->$var.name$$endif$);$endif$};separator="\n"$
                $class.objects.values:{ var | \$clone->$var.name$ = \$this->$var.name$->clone();};separator="\n"$
                $class.collections.values:{ var | foreach( \$this->$var.name$ as \$obj ){array_push(\$clone->$var.name$,\$obj->clone());}};separator="\n"$
        	return \$clone;
        }
        
        public function equals(\$valueObject)
        {
                $class.variables.values:{ var | if(\$valueObject->$var.name$ != \$this->$var.name$){ return false; }};separator="\n"$
                $class.properties.values:{ var | $if(var.readable)$if(\$valueObject->get$var.capitalize$() != \$this->get$var.capitalize$()){ return false; }$endif$};separator="\n"$
                $class.objects.values:{ var | if(!\$valueObject->$var.name$->equals(\$this->$var.name$)){ return false; }};separator="\n"$
                $class.collections.values:{ var | for( \$x = 0; \$x <= array_len(\$valueObject->$var.name$); \$x++ ){if(!\$valueObject->$var.name$[\$x]->equals(\$this->$var.name$[\$x])){ return false; }}};separator="\n"$
        	return true;
        }
        
        public function toString()
        {
        	var \$out;
                $class.variables.values:{ var | \$out .= "$var.capitalize$: " . \$this->$var.name$ . "\\n";};separator="\n"$
                $class.properties.values:{ var | $if(var.readable)$\$out .= "$var.capitalize$: " . \$this->get$var.capitalize$() . "\\n";$endif$};separator="\n"$
                $class.objects.values:{ var | \$out .= "\\t$var.capitalize$: " . \$this->$var.name$->toString() . "\\n";};separator="\n"$
                $class.collections.values:{ var | foreach( \$this->$var.name$ as \$obj ){\$out .= "\\t" . \$obj->toString();}};separator="\n"$
        	return \$out;
        }
        
        public function toXML()
        {
        	var \$xml = "<$class.name$>";
                $class.variables.values:{ var | \$xml .= "\\t<$var.name$>" . \$this->$var.name$ . "</$var.name$>\\n";};separator="\n"$
                $class.properties.values:{ var | $if(var.readable)$\$xml .= "\\t<$var.name$>" . \$this->get$var.capitalize$() . "</$var.name$>\\n";$endif$};separator="\n"$
                $class.objects.values:{ var | \$xml .= "\\t\\t" . \$this->$var.name$->toXML() . "\\n";};separator="\n"$
                $class.collections.values:{ var | foreach( \$this->$var.name$ as \$obj ){\$out .= "\\t" . \$obj->toXML();}};separator="\n"$
                \$xml = "</$class.name$>";
        	return \$xml;
        }
}

?>