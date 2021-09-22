import React, {Component} from 'react';
import { withRouter  } from "react-router-dom"

class Category extends Component {

    state={
        children_category: [],
        parent_category :[],
        products :[]
    }
    async call_server() {
        const parents_raw =  await fetch(`http://127.0.0.1:8000/category/${this.props.match.params.id}/all_parents/`)
        const parents = await parents_raw.json()
        const state_parent = []
        for(let parent of parents){
            state_parent.push(parent)
        }
        const children_raw =  await fetch(`http://127.0.0.1:8000/category/${this.props.match.params.id}/children/`)
        const children = await children_raw.json()
        const children_state = []
        for(let child of children){
            children_state.push(child)
        }

        this.setState({
            parent_category: state_parent,
            children_category : children_state
        })

    }

    componentDidMount() {
        this.call_server()
    }
    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.match.params.id !== this.props.match.params.id){
            this.call_server()
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