import React, {Component} from 'react';

class Options extends Component {
    state = {
        option: [],
        delivery: []
    }

    handleDelivery = (data) => {
        this.setState({delivery: data})
    }
    handleOption =(data)=>{
        this.setState({option:data})
    }
    generateDelivery = () => {
        const url = 'http://127.0.0.1:8000/card/delivery/'
        fetch(url).then(response => response.json()).then(data => this.handleDelivery(data))
        const url2 = 'http://127.0.0.1:8000/card/options/'
        fetch(url2).then(response => response.json()).then(data =>this.handleOption(data))
    }

    render() {
        return (
            <div>
                <select name='delivery' id='delivery'>
                    {this.state.delivery && this.state.delivery.map((delivery, index) => {
                        return <option key={index} name={delivery.id} id={delivery.id}
                                       data-price={delivery.price}>{delivery.name}</option>
                    })}
                </select>
                <select name='option' id='option'>
                    {this.state.option && this.state.option.map((option, index) => {
                        return <option key={index} name={option.id} id={option.id}
                                       data-price={option.price}>{option.name}</option>
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