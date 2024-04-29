import { Link } from "react-router-dom";



const QuickLink = (props) => {
    
    //direction, icon, text, pathname
    
    
    return <li className="quick-link">
        <Link to={props.direct} 
            className={props.pathname === props.direct ? "active"  : ""}>
            {props.icon} {props.text}
        </Link>
    </li>;
};

export default QuickLink;
