import React, {Component} from 'react';
import {withRouter} from "react-router-dom"

class Category extends Component {
    constructor(props) {
        super(props);
        this.get_products = this.get_products.bind(this)
    }

    state = {
        children_category: [],
        parent_category: [],
        products: [],
        page: 1,
        per_page: 10,
        order_by: "created_time"
    }

    async get_category() {
        const parents_raw = await fetch(`http://127.0.0.1:8000/category/${this.props.match.params.id}/all_parents/`)
        const parents = await parents_raw.json()
        const state_parent = []
        for (let parent of parents) {
            state_parent.push(parent)
        }
        const children_raw = await fetch(`http://127.0.0.1:8000/category/${this.props.match.params.id}/children/`)
        const children = await children_raw.json()
        const children_state = []
        for (let child of children) {
            children_state.push(child)
        }

        this.setState({
            parent_category: state_parent,
            children_category: children_state
        })

    }

    async get_products() {
        const low = ((this.state.page - 1) * this.state.per_page)
        const high = (this.state.page * this.state.per_page) - 1
        const url = `http://127.0.0.1:8000/product/find/?category=${this.props.match.params.id}&sortby=-${this.state.order_by}&low=${low}&high=${high}`
        const products_raw = await fetch(url)
        const products = await products_raw.json()
        const state_product = []
        for (let product of products) {
            state_product.push(product)
        }
        this.setState({products: state_product})
    }

    componentDidMount() {
        this.get_category()
        this.get_products()
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.match.params.id !== this.props.match.params.id) {
            this.get_category()
            this.get_products()
        } else {
            if (prevState.page !== this.state.page || prevState.per_page !== this.state.per_page) {
                this.get_products()
            }
        }
    }

    render() {
        // this.call_server()
        return (
            <div>
                {/*{this.call_server()}*/}
            </div>
        );
    }
}

export default withRouter(Category);