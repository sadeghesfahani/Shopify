import React, {Component} from 'react';

class Options extends Component {
    state = {
        option: [],
        delivery: []
    }

    handleDelivery = (data) => {
        if (data[0]){

            this.setState({delivery: data})
        this.props.delivery({id: data[0].id, price: data[0].price})
        }

    }
    handleOption = (data) => {
        if(data[0]){

            this.setState({option: data})
            this.props.option({id:data[0].id,type:data[0].option_type,price:data[0].cost})
        }
    }
    generateDelivery = () => {
        const url = 'http://127.0.0.1:8000/card/delivery/'
        fetch(url).then(response => response.json()).then(data => this.handleDelivery(data))
        const url2 = 'http://127.0.0.1:8000/card/options/'
        fetch(url2).then(response => response.json()).then(data => this.handleOption(data))
    }

    deliveryChange = (e) => {
        const data = {
            id: e.target.options[e.target.selectedIndex].id,
            price: e.target.options[e.target.selectedIndex].dataset.price
        }
        console.log(data)
        this.props.delivery(data)
    }

    optionChange = (e) => {
        const data = {
            id: e.target.options[e.target.selectedIndex].id,
            price: e.target.options[e.target.selectedIndex].dataset.price,
            type:e.target.options[e.target.selectedIndex].dataset.optiontype
        }
        console.log(data)
        this.props.option(data)
    }

    render() {
        return (
            <div>
                <select onChange={this.deliveryChange} name='delivery' id='delivery'>
                    {this.state.delivery && this.state.delivery.map((delivery, index) => {
                        return <option key={index} name={delivery.id} id={delivery.id}
                                       data-price={delivery.price}>{delivery.name}</option>
                    })}
                </select>
                <select onChange={this.optionChange} name='option' id='option'>
                    {this.state.option && this.state.option.map((option, index) => {
                        return <option key={index} name={option.id} id={option.id}
                                       data-price={option.cost}
                                       data-optiontype={option.option_type}>{option.name}</option>
                    })}
                </select>
            </div>
        );
    }

    componentDidMount() {
        this.generateDelivery()
    }
}

export default Options;