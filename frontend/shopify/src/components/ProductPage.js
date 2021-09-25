import React, {Component} from 'react';
import {withRouter} from "react-router-dom";

class ProductPage extends Component {
    constructor(props) {
        super(props);

        this.getProductInfo = this.getProductInfo.bind(this)
    }
    state = {
        product:{}
    }

    async getProductInfo() {
        console.log('here')
        const url = `http://127.0.0.1:8000/product/${this.props.match.params.id}/`
        const result = await fetch(url)
        const productInfo = await result.json()
        this.setState({product:productInfo})
    }



    generateCarousel=()=>{

        return(
            <div id="carouselExampleIndicators" className="carousel slide" data-ride="carousel">
                <ol className="carousel-indicators">
                    <li data-target="#carouselExampleIndicators" data-slide-to="0" className="active"/>
                    {this.state.product.media && this.state.product.media.map((picture,index)=>{
                        <li key={index} data-target="#carouselExampleIndicators" data-slide-to={index+1}/>
                    })}
                </ol>
                <div className="carousel-inner">
                    <div className="carousel-item active">
                        <img className="d-block w-100" src={`http://127.0.0.1:8000${this.state.product.image}`} alt="First slide"/>
                    </div>
                    <div className="carousel-item">
                        <img className="d-block w-100" src="..." alt="Second slide"/>
                    </div>
                    <div className="carousel-item">
                        <img className="d-block w-100" src="..." alt="Third slide"/>
                    </div>
                </div>
                <a className="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"/>
                    <span className="sr-only">Previous</span>
                </a>
                <a className="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"/>
                    <span className="sr-only">Next</span>
                </a>
            </div>
        )
    }

    render() {
        return (
            <div className='row'>
                <div className='col-12 col-lg-6'>
                    {this.generateCarousel()}
                </div>
                <div className='col-12 col-lg-6'>

                </div>
            </div>
        );
    }
    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.match && prevProps.match.params.id !== this.props.match.params.id){
            this.getProductInfo()
        } else{
            if (prevProps.match === undefined){
                this.getProductInfo()
            }
        }
    }
    componentDidMount() {
        this.getProductInfo()
    }
}

export default withRouter(ProductPage);