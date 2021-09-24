import React, {Component} from 'react';
import {Link} from "react-router-dom";

class Subcategory extends Component {
    render() {
        return (
            <div className='col-12 p-0 '>
                <ul className="list-group p-0 m-0">
                    {this.props.subcategories.map((category,index)=>{
                        return(
                            <Link to={`/category/${category.id}`} ><li key={index} className="list-group-item">{category.name}</li></Link>
                        )
                    })}
                </ul>
            </div>
        );
    }
}

export default Subcategory;