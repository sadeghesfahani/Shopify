import React, {Component} from 'react';
import {withRouter} from "react-router-dom";

class ProductPage extends Component {
    constructor(props) {
        super(props);

        this.getProductInfo = this.getProductInfo.bind(this)
    }

    state = {
        product: {},
        option: 0
    }

    handleOptionChange = (id) => {
        const select = document.getElementById(id)
        const value = select.options[select.selectedIndex].value
        for (let option of this.state.product.attributes[0].options) {
            console.log(value)
            console.log(option)
            if (option.id == value) {
                this.setState({option: option})
            }
        }

    }

    async getProductInfo() {
        console.log('here')
        const url = `http://127.0.0.1:8000/product/${this.props.match.params.id}/`
        const result = await fetch(url)
        const productInfo = await result.json()
        this.setState({product: productInfo})
        this.setState({option: this.state.product.attributes[0]!==undefined ? this.state.product.attributes[0].options[0] : false})
    }

    generatePrice = () => {
        if (this.state.option) {
            if (this.state.option.type === 0) {
                return this.state.product.price
            } else if (this.state.option.type === 1) {
                return this.state.option.price
            } else if (this.state.option.type === 2) {
                return this.state.product.price + this.state.option.price
            } else if (this.state.option.type === 3) {
                return (1 + this.state.option.price / 100) * this.state.product.price
            }

        } else {
            return this.state.product.price
        }
    }

    handleAddToCard = () => {
        const card_raw = localStorage.getItem('card')
        const card = JSON.parse(card_raw)
        if (card !== null) {
            let doesProductExist = false
            for (let product of card.orders) {
                if (product.product === this.state.product.id) {
                    if (product.option === this.state.option.id) {
                        doesProductExist = true
                    }

                }
            }
            if (!doesProductExist) {
                card.orders.push({product: this.state.product.id, option: this.state.option.id})
                localStorage.setItem('card', JSON.stringify(card))
            }
        } else {
            const new_card = {orders: []}
            new_card.orders.push({product: this.state.product.id, option: this.state.option.id})
            localStorage.setItem('card', JSON.stringify(new_card))
        }

    }

    generateInfo = () => {
        return (
            <div>
                <h1>{this.state.product.name}</h1>
                <h2>{this.generatePrice()}</h2>
                {this.state.product.attributes && this.state.product.attributes.map((attr, index) => {
                    return (
                        <>
                            <label htmlFor={attr.id}>{attr.name}</label>
                            <select id={attr.id} onChange={() => this.handleOptionChange(attr.id)}>
                                {attr.options && attr.options.map((opt, indexopt) => {
                                    return <option value={opt.id} key={indexopt}>{opt.name}</option>
                                })}
                            </select>
                        </>
                    )
                })}
                <button onClick={this.handleAddToCard} className='btn btn-primary'>افزوردن به سبد خرید</button>
            </div>
        )
    }

    generateCarousel = () => {

        return (
            <div id="carouselExampleIndicators" className="carousel slide" data-ride="carousel">
                <ol className="carousel-indicators">
                    <li data-target="#carouselExampleIndicators" data-slide-to="0" className="active"/>
                    {this.state.product.media && this.state.product.media.map((picture, index) => {
                        return <li key={index} data-target="#carouselExampleIndicators" data-slide-to={index + 1}/>
                    })}
                </ol>
                <div className="carousel-inner">
                    <div className="carousel-item active">
                        <img className="d-block w-100" src={`http://127.0.0.1:8000${this.state.product.image}`}
                             alt="First slide"/>
                    </div>
                    {this.state.product.media && this.state.product.media.map((picture, index) => {
                        return (
                            <div className="carousel-item">
                                <img className="d-block w-100" src={`http://127.0.0.1:8000${picture}`}/>
                            </div>
                        )

                    })}

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
                    {this.generateInfo()}
                </div>
            </div>
        );
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.match && prevProps.match.params.id !== this.props.match.params.id) {
            this.getProductInfo()
        } else {
            if (prevProps.match === undefined) {
                this.getProductInfo()
            }
        }
    }

    componentDidMount() {
        this.getProductInfo()
    }
}

export default withRouter(ProductPage);